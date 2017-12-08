'''
Flexible Origin Controller program file

Process the request from flask and call sub classes

Author: XAP

Version: 1.0

Change logger:
2017-12-04 - Adding TechJam2017 code
2017-11-29 - First version
'''

from werkzeug.local import LocalProxy
from flask.wrappers import Response

from fostatuscode import FOStatusCode
from foheader import FOHeader
from fobody import FOBody
from foaction import FOAction
from foerrors import HeaderError

# import logging
from fologger import FOLogger


class FOController(object):
    # Must be in lower case
    _HEADER_PREFIX = 'x-fo-'

    _request = None
    _response = None
    _x_fo_headers = dict()
#    _x_fo_headers_list = list()

    def __init__(self, log_file=None, log_level=40):
        """Start the request processing

        This function starts the Flexible Origin work

        Keywords:
        log_file - file to store logs
        log_level - verbosity

        Returns:
        None
        """
        self._log_obj = FOLogger('FOController', log_file, log_level)
        self._logger = self._log_obj.logger

    @property
    def request(self):
        """Getter for the request object
        Returns:
        _request
        """
        if self._request is None:
            raise TypeError('No request available')
        return self._request

    @request.setter
    def request(self, request):
        """Set the internal request variable
        Keyword Arguments:
        request -- Flask request value

        Returns:
        0 -- int
        """
        if isinstance(request, LocalProxy):
            self._request = request
        else:
            raise TypeError('request type is not werkzeug compatible')

        return 0

    @property
    def response(self):
        """getter for response object

        returns
        _response
        """
        if self._response is None:
            raise TypeError('no response available')
        return self._response

    @response.setter
    def response(self, response):
        """setter for response object
        keyword arguments:
        response -- response object

        returns
        0 --int
        """
        if isinstance(response, Response):
            self._response = response
        else:
            raise TypeError('response type is not Flask compatible')

        return 0

    def _load_x_fo_headers(self):
        """extract x-fo-* headers from request

        extract the x-fo headers from request, change to lower case
        and store those in a new dictionary and list:

        self._x_fo_headers -- dict for header information
        self._x_fo_headers_list -- list for the unique headers in request

        returns
        0 -- int
        """
        self._x_fo_headers.clear()
        for header, value in self.request.headers.items():
            header_low = header.lower()
            self._logger.debug('Header: %s, value: %s', header_low, value)
            if self._HEADER_PREFIX in header_low:
                self._x_fo_headers[header_low] = value
#                self._x_fo_headers_list.append(header_low)
        if len(self._x_fo_headers) < 1:
            raise HeaderError('No {}* headers found in the request'.format(
                self._HEADER_PREFIX))

        return 0

    def process(self, request, response):
        """Call subclases to execute x-fo header commands

        Executes the commands required by x-fo headers

        Keywords:
        request -- request HTTP object
        response -- response HTTP onject

        Returns:
        0 -- int
        """
        self.request = request
        self.response = response
        try:
            self._load_x_fo_headers()
        except HeaderError as e:
            # If an error is found, a default header is set
            m = 'X-FO-Warning={}'.format(e.args[0])
            self._x_fo_headers['x-fo-header-add'] = m
            self._x_fo_headers['x-fo-body-info'] = 'html'

        def class_selector(x_fo_header_name):
            """ maps the header name with the python class """
            try:
                fo_class_name = x_fo_header_name.split('-')[2]
            except:
                m = 'Header name: {} is not property formed, '
                m += 'make sure format is {}-Class-Action=value'
                m = format(x_fo_header_name, self._HEADER_PREFIX.title())
                raise HeaderError(m)
            try:
                fo_class_case = {
                    'statuscode': FOStatusCode,
                    'header': FOHeader,
                    'body': FOBody,
                    'action': FOAction
                }[fo_class_name]
            except:
                m = 'This control header is not supported: {}'
                m = m.format(x_fo_header_name)
                raise HeaderError(m)
            return fo_class_case

        for fo_header_name, fo_header_value in self._x_fo_headers.items():
            fo_class = class_selector(fo_header_name)()
            fo_method_name = fo_header_name.split('-')[3]
            r = getattr(fo_class, fo_method_name)(self.request,
                                                  self.response,
                                                  fo_header_value)
            del fo_class
            self.response = r
        return 0
