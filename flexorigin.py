'''
Flexible Origin main program file

This tool allows the user control the res_test by sending headers
in the request.

This code works for origin mode.

Author: XAP

Modules required: flask
pip install --user flask


Version: 1.0

Change log:
2017-12-04 - Adding TechJam code
2017-11-29 - First version
'''

from flask import Flask, request, make_response, jsonify
from flask import render_template, url_for, redirect
from focontroller import FOController
from fologger import FOLogger
from foerrors import HeaderError
import os
from werkzeug import secure_filename
from random import randint

# Define the script's root path
prog_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
# app.config['SERVER_NAME'] = 'localhost:5000'
LOG_FILE = '{}/static/fo.log'.format(prog_path)
LOG_LEVEL = {'error': 40, 'warning': 30, 'info': 20, 'debug': 10}['info']
# Init the Logger object
obj_log = FOLogger('FlexOrigin', LOG_FILE, LOG_LEVEL)
logger = obj_log.logger

# Starts the controller
flex_controller = FOController(log_object=obj_log)



# Exception Class
class InvalidUsage(Exception):
    """Generic Exception Class for Error Handling"""
    _status_code = 400
    _message = 'Internal Flexible Origin Error'
    _payload = {'error': 'Internal FlexOrigin Error'}

    def __init__(self, message, status_code=None, payload=None):
        """ Init the Exception Class """
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        logger.error(message)

    @property
    def message(self):
        """Getter for message
        Returns:
        _message
        """
        return self._message

    @message.setter
    def message(self, message):
        """Setter for message
        Keyword Arguments:
        message -- str
        Returns:
        0 -- int
        """
        if message is not None:
            self._message = message
        return 0

    @property
    def status_code(self):
        """Getter for status_code
        Returns:
        _status_code
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """Setter for status_code
        Keyword Arguments:
        status_code -- str
        Returns:
        0 -- int
        """
        if status_code is not None:
            self._status_code = status_code
        return 0

    @property
    def payload(self):
        """Getter for payload
        Returns:
        _payload
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """
        Keyword Arguments:
        payload -- str

        Returns:
        0 -- int
        """
        if payload is not None:
            self._payload = payload
        return 0

    def to_dict(self):
        """Create a dictionary for error info
        Returns:
        dict
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# Exception Reguster
@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    error_dict = error.to_dict()
    response = jsonify(error_dict)
    response.status_code = error.status_code
    response.headers['Server'] = 'FlexibleOrigin'
    response.headers['X-FO-Error'] = error_dict
    return response


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def flexorigin(subpath=None):
    """flexorigin

    Ths function process any request path, end request object to controller
    and return the generated res_test.

    Keywords Arguments:
    subpath -- str, path string (default = None)

    Return:
    html res_test
    """

    # Generate the Reference ID number
    referenceid = randint(10000, 99999)
    reference_str = 'RefID:{}'.format(referenceid)

    # Set Log ReferenceID
    obj_log.log_name = reference_str

    http_request = request
    # default response: empty body and status code 200
    # TODO: Import defaults from config file
    http_response = make_response('This is a Flexible Origin response\n')
    http_response._status_code = 200
    http_response.headers['Server'] = 'FlexibleOrigin'
    try:
        flex_controller.process(http_request, http_response)
        http_response = flex_controller.response
    except HeaderError as e:
        host_name = http_request.headers['host']
        desc = {'X-FO header problem': 'Bad name or value',
                'Help': 'Go to {}/static/help.html'.format(host_name),
                'RefID': referenceid}
        raise InvalidUsage(e.args[0], payload=desc)
    except Exception as e:
        desc = {'RefID': referenceid}
        raise InvalidUsage(e.args[0], payload=desc)
    else:
        http_response.headers['X-FO-RefID'] = referenceid
    return http_response


@app.route('/x-fo/pushasset', methods=['GET', 'POST'])
def uploader():
    _user_path = '{}/user/'.format(prog_path)
    # TODO: Refactor code
    if request.method == 'POST':
        savepath = _user_path
        f = request.files['file']
        if request.args.get('filename'):
            f.filename = str(request.args.get('filename'))
        if request.form['path']:
            savepath = _user_path + str(request.form['path']) + "/"
            if not os.path.exists(savepath):
                os.makedirs(savepath)
        if request.args.get('path'):
            savepath = _user_path + str(request.args.get('path')) + "/"
            if not os.path.exists(savepath):
                os.makedirs(savepath)
        f.save(savepath + secure_filename(f.filename))
    return redirect(url_for('upload_file'))


@app.route('/x-fo/upload')
def upload_file():
    host = request.headers['host']
    path = url_for('uploader')
    return render_template('upload.html', host=host,
                           path=path)
