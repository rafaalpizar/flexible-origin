'''
Flexible Origin Status Code Class

This class handle the Status code from Flexible Origin headers commands

Author: Rafael Alpizar L

Version: 1.0

Change log:
2017-11-24 - First version
'''


class FOStatusCode(object):
    """Object to handle Response Status Code in Flexible Origin"""

    _MIN_STATUS_VALUE = 0
    _MAX_STATUS_VALUE = 599

    def __init__(self):
        """Init the object
        Nothing to do yet
        """
        pass

    def define(self, request, response, new_status_code):
        """Sets the response status code

        Keyword Arguments:
        request    -- request object
        response   -- base response object
        new_status_code -- new header to add to response

        Returns:
        response   -- altered response object
        """
        error = False
        status_value = int(new_status_code)
        if status_value < self._MIN_STATUS_VALUE:
            error = True
        if status_value > self._MAX_STATUS_VALUE:
            error = True
        if error:
            m = 'New Status Code value is out of range. '
            m += 'Allowed values are {}..{}'.format(self._MIN_STATUS_VALUE,
                                                    self._MAX_STATUS_VALUE)
            raise ValueError(m)
        response.status_code = status_value
        return response
