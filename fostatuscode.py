'''
Flexible Origin Status Code Class

This class handle the Status code from Flexible Origin headers commands

Author: Rafael Alpizar L

Version: 1.0

Change log:
2017-11-24 - First version
'''

from foerrors import HeaderError


class FOStatusCode(object):
    """Object to handle Response Status Code in Flexible Origin"""

    _MIN_STATUS_VALUE = 0
    _MAX_STATUS_VALUE = 599

    def __init__(self, log_object=None):
        """Init the object

        Keywords:
        log_object - logger object

        Returns:
        None
        """
        self._log_obj = log_object
        self._logger = self._log_obj.logger
        self._logger.debug('Running Flexible Origin status code modification')

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
        try:
            status_value = int(new_status_code)
        except:
            m = 'The Status Code value {} is invalid, '
            m += 'it must be a positive integer.'
            m = m.format(new_status_code)
            raise HeaderError(m)
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
