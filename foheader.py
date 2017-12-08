'''
Flexible Origin Header Class

This class handle the Headers from Flexible Origin headers commands

Author: XAP

Version: 1.0

Change log:
2017-12-04 - Adding TechJam2017 code
2017-11-29 - First version
'''

from foerrors import HeaderError


class FOHeader(object):
    """Object to handle headers in Flexible Origin"""

    def __init__(self):
        """Starts the object
        init stuff
        """
        pass

    def add(self, request, response, new_header):
        """Adds a header to response object
        New header must be in format:
        header=value

        Keyword Arguments:
        request    -- request object
        response   -- base response object
        new_header -- new header to add to response

        Returns:
        response   -- altered response object
        """
        try:
            nheader_name, nheader_val = new_header.split('=', 1)
        except:
            m = 'Error extracting new header information from: {}, '
            m += 'make sure format is header=value'
            m = m.format(new_header)
            raise HeaderError(m)
        response.headers.add(nheader_name, nheader_val)
        return response

    def addcookie(self, request, response, new_cookie):
        """Adds a Cookie to response objects
        Create a new header Set-Cookie with the value as new_cookie

        Keyword Arguments:
        request    -- request object
        response   -- response object
        new_cookie -- new cookie value

        Returns:
        response   -- altered response object
        """
        response.headers.add('Set-Cookie', new_cookie)
        return response

    def modify(self, request, response, new_header):
        """Modify a header in response objects
        Modify an existing header in the response
        and if the header does not exists it create a new one

        Keyword Arguments:
        request    -- request object
        response   -- response object
        new_cookie -- new cookie value

        Returns:
        response   -- altered response object
        """
        try:
            nheader_name, nheader_val = new_header.split('=', 1)
        except:
            m = 'Error extracting modify header information from: {}, '
            m += 'make sure format is header=value'
            m = m.format(new_header)
            raise HeaderError(m)
        response.headers[nheader_name] = nheader_val
        return response
