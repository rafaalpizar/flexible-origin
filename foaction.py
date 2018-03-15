'''
Flexible Origin Status Code Class

This class handles the server manipulation actions from
Flexible Origin headers commands

Author: X-Akamai-Projects

Version: 1.0

Change log:
2017-11-29 - First version
'''

import time
from foerrors import HeaderError


class FOAction(object):
    """Object to handle server manipulation actions in Flexible Origin"""

    def __init__(self, log_object=None):
        """Init the object

        Keywords:
        log_object - logger object

        Returns:
        None
        """
        self._log_obj = log_object
        self._logger = self._log_obj.logger
        self._logger.debug('Running Flexible Origin action')

    def delay(self, request, response, delay_value):
        """Delays the response by applying a sleep timer.

        Keyword Arguments:
        delay_value -- delay in seconds on response

        Returns:
        response -- Flask response object
        """
        _MIN_DELAY = 0
        try:
            delay_int = int(delay_value)
        except ValueError:
            m = 'Wrong header value: {}, '.format(delay_value)
            m += 'only positive interger are supported'
            raise HeaderError(m)
        if delay_int < _MIN_DELAY:
            m = 'Delay timer value must be a positive integer'
            raise HeaderError(m)

        time.sleep(delay_int)

        return response
