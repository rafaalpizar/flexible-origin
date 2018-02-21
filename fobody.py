'''
Flexible Origin Body Class

This class handle the Body from Flexible Origin headers commands

Author: XAP

Version: 1.0

Change log:
2017-12-04 - Adding TechJam2017 code
2017-11-29 - First version
'''

import json
from foerrors import HeaderError
from flask import send_file, render_template
import os
import re

prog_path = os.path.dirname(os.path.realpath(__file__))


class FOBody(object):
    """Object to handle Response Body in Flexible Origin"""

    _HELP_FILE = '{}/static/help.html'.format(prog_path)
    _LOG_FILE = '{}/static/fo.log'.format(prog_path)

    def __init__(self, log_object=None):
        """Init the object

        Keywords:
        log_object - logger object

        Returns:
        None
        """
        self._log_obj = log_object
        self._logger = self._log_obj.logger
        self._logger.debug('Running Flexible Origin body modification')


    def _header_to_json(self, headers):
        """Read headers dictionary an creates a json format string
        Keyword Arguments:
        headers -- dict

        Returns:
        str
        """
        return json.dumps(headers)

    def _header_to_plain(self, headers):
        """Read headers dictionary an creates a plain format string
        Keyword Arguments:
        headers -- dict

        Returns:
        str
        """
        strbody = ''
        for header, value in headers.items():
            strbody += '{}: {}\n'.format(header, value)
        return strbody

    def _header_to_xml(self, headers):
        """Read headers dictionary an creates a xml format string
        Keyword Arguments:
        headers -- dict

        Returns:
        str
        """
        strbody = '<headers>\n'
        for header, value in headers.items():
            strbody += '<{}>{}</{}>\n'.format(header, value, header)
        strbody += '</headers>\n'
        return strbody

    def _header_to_html(self, headers):
        """Read headers dictionary an creates a html format string
        Keyword Arguments:
        headers -- dict

        Returns:
        str
        """
        strbody = '<table>\n'
        strbody += '<thead><tr><th>Field</th><th>Value</th></tr></thead>\n'
        strbody += '<tbody>\n'
        for header, value in headers.items():
            l = '<tr><td>{}</td><td>{}</td></tr>\n'.format(header, value)
            strbody += l
        strbody += '</tbody></table>\n'
        return strbody

    def showrequestheaders(self, request, response, strformat):
        """Fill the respose body with the request headers
        Keyword Arguments:
        request  -- request object
        response -- response onject
        switch   -- (default Off)

        Returns:
        response -- Flaks response object
        """

        def to_json(headers):
            return self._header_to_json(headers)

        def to_plain(headers):
            return self._header_to_plain(headers)

        def to_xml(headers):
            strbody = '<?xml version="1.0" encoding="UTF-8"?>\n'
            strbody += '<root>\n'
            strbody += self._header_to_xml(headers)
            strbody += '</root>'
            return strbody

        def to_html(hostname, headers):
            strtable = self._header_to_html(headers)
            html_res = render_template('header_table.html',
                                       hostname=hostname, table=strtable)
            return html_res

        body = ''
        headers_dict = dict(request.headers)
        supported_formats = ['json', 'plain', 'html', 'xml']
        if strformat not in supported_formats:
            m = 'Body format is not allowed: {}. '
            m += 'Supported formats are: {}'
            m = m.format(strformat, ','.join(supported_formats))
            raise HeaderError(m)
        hostname = request.host
        body = {
            'json': to_json(headers_dict),
            'plain': to_plain(headers_dict),
            'xml': to_xml(headers_dict),
            'html': to_html(hostname, headers_dict)
            }[strformat]
        response.data = body
        return response

    def showrequestbody(self, request, response, strformat):
        """Fill the response body with the request body
        Keyword Arguments:
        request   -- request object
        response  -- response object
        strformat -- (default same)

        Returns:
        response -- Flaks response object
        """
        response.data = request.get_data()
        return response

    def info(self, request, response, strformat):
        """Fill the respose body with the request/response information
        Keyword Arguments:
        request  -- request object
        response -- response onject
        strformat -- srt

        Returns:
        response -- Flaks response object
        """

        def to_json(headers):
            return self._header_to_json(headers)

        def to_plain(headers):
            return self._header_to_plain(headers)

        def to_xml(headers):
            strbody = '<?xml version="1.0" encoding="UTF-8"?>\n'
            strbody += '<root>\n'
            strbody += self._header_to_xml(headers)
            strbody += '</root>'
            return strbody

        def to_html(hostname, headers):
            strtable = self._header_to_html(headers)
            html_res = render_template('request_info.html',
                                       hostname=hostname, table=strtable)
            return html_res

        def to_help():
            html_help = send_file(self._HELP_FILE)
            html_help.direct_passthrough = False
            return html_help.data

        supported_formats = ['json', 'plain', 'html', 'xml', 'help']
        body = ''
        headers_dict = dict()
        headers_dict['Incoming URL'] = request.url
        headers_dict['Incoming Method'] = request.method
        headers_dict['Client IP'] = request.remote_addr
        headers_dict.update(dict(request.headers))
        if strformat not in supported_formats:
            m = 'Body format is not allowed: {}. '
            m += 'Supported formats are: {}'
            m = m.format(strformat, ','.join(supported_formats))
            raise HeaderError(m)
        hostname = request.host
        body = {
            'json': to_json(headers_dict),
            'plain': to_plain(headers_dict),
            'xml': to_xml(headers_dict),
            'html': to_html(hostname, headers_dict),
            'help': to_help()
            }[strformat]
        response.data = body
        return response

    def image(self, request, response, imagetype):
        """Fill the respose body with the request headers
        Keyword Arguments:
        request  -- request object
        response -- response onject
        imagetype -- str

        Returns:
        response -- Flask http response
        """
        supported_formats = ['png', 'gif', 'jpeg']
        if imagetype not in supported_formats:
            m = 'Image format is not allowed: {}. '
            m += 'Supported formats are: {}'
            m = m.format(imagetype, ','.join(supported_formats))
            raise HeaderError(m)
        asset = {'png': 'assets/images/xap.png',
                 'gif': 'assets/images/xap.gif',
                 'jpeg': 'assets/images/xap.jpeg'}[imagetype]
        body = send_file(asset)
        body.direct_passthrough = False
        response.data = body.data
        return response

    def loglines(self, request, response, lines):
        """Return log lines in response body
        Keyword Arguments:
        request  -- request object
        response -- response onject
        lines    -- str, number of lines to be returned

        Returns:
        response -- Flask response object
        """
        try:
            num_lines = int(lines)
        except:
            m = 'Invalid value: {}, '.format(lines)
            m += 'Allowed only positive integers'
            raise HeaderError(m)
        if num_lines < 1:
            m = 'Number: {}, is invalid. '.format(num_lines)
            m += 'Allowed values more than or equal to 1'
            raise HeaderError(m)
        with open(self._LOG_FILE, 'r') as log_fh:
            log_lines = log_fh.readlines()
        start = len(log_lines) - num_lines
        body = ''
        while len(log_lines) > start:
            body = log_lines.pop() + body
        response.data = body
        return response

    def compressed(self, request, response, compresstype):
        """Fill the respose body with a specific compressed object
        Keyword Arguments:
        request  -- request object
        response -- response onject
        compresstype -- file type

        Returns:
        response -- Flask response object
        """
        supported_formats = ['zip', 'gzip', 'bzip', 'deflate', 'br']
        if compresstype not in supported_formats:
            m = 'Compress format is not allowed: {}. '
            m += 'Supported formats are: {}'
            m = m.format(compresstype, ','.join(supported_formats))
            raise HeaderError(m)
        asset = {'zip': 'assets/compressed/xap.zip',
                 'gzip': 'assets/compressed/xap.gz',
                 'bzip': 'assets/compressed/xap.bz',
                 'deflate': 'assets/compressed/xap.deflate',
                 'br': 'assets/compressed/xap.br'}[compresstype]
        temp_response = send_file(asset)
        temp_response.direct_passthrough = False
        response.data = temp_response.data
        return response

    def binary(self, request, response, sizeinbytes):
        """Fill the respose body with binary content
        Keyword Arguments:
        request  -- request object
        response -- response onject
        sizeinbytes - number of bytes for size

        Returns:
        response -- Flask response object
        """
        _MIN_SIZE = 0

        try:
            size_int = int(sizeinbytes)
        except:
            m = 'Number: {}, is invalid. '.format(sizeinbytes)
            m += 'Allowed values more than or equal to 1'
            raise HeaderError(m)
        if size_int < _MIN_SIZE:
            m = 'Requested size in bytes {} is less than minimun {}'
            m = m.format(size_int, _MIN_SIZE)
            raise HeaderError(m)
        binary_stream = open("/dev/urandom", "rb").read(size_int)
        response.data = binary_stream
        return response

    def text(self, request, response, texttype):
        """Fill the respose body with text
        Keyword Arguments:
        request  -- request object
        response -- response onject
        texttype   -- kind of text required
        """
        supported_formats = ['css', 'html', 'indexhtml', 'js', 'plain']
        if texttype not in supported_formats:
            m = 'Text format is not allowed: {}. '
            m += 'Supported formats are: {}'
            m = m.format(texttype, ','.join(supported_formats))
            raise HeaderError(m)
        asset = {'css': 'assets/texts/xap.css',
                 'html': 'assets/texts/xap.html',
                 'indexhtml': 'assets/texts/xapindex.html',
                 'js': 'assets/texts/xap.js',
                 'plain': 'assets/texts/xap.txt'}[texttype]
        temp_response = send_file(asset)
        temp_response.direct_passthrough = False
        response.data = temp_response.data
        return response

    def path(self, request, response, urlpath):
        """Fill the respose body with the request headers
        Keyword Arguments:
        request  -- request object
        response -- response onject
        urlpath   -- str, define if urlpath will be used

        Returns:
        response -- Flask response object
        """
        # TODO: Refector code
        _user_path = 'user/'
        if "true" in urlpath:
            if request.path:
                validpath = re.sub('/$', "/index.html", request.path)
            if os.path.exists(_user_path+validpath) and \
                    not os.path.isdir(_user_path+validpath):
                temp_response = send_file(_user_path+validpath)
                # TODO: Temporal fix
                temp_response.direct_passthrough = False
                response.data = temp_response.data
                # Minimum request headers required
                response.headers["Content-Type"] = \
                    temp_response.headers["Content-Type"]
            else:
                m = 'The path {} was not found. '
                m += 'You might want to upload it first'
                m = m.format(_user_path+validpath)
                raise HeaderError(m)
        return response
