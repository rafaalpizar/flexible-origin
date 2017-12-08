'''
Flexible Origin Logging Class

To handle the logging methods

Author: Rafael Alpizar L

Version: 1.0

Change log:
2017-11-24 - First version
'''

import logging


class FOLogger(object):
    """ Cusom Logging class """

    def __init__(self, log_name='LogName', log_file=None, log_level=40):
        """Init Logging parameters

        Set the log parameters, if log_file is None then the lines will be written
        in stdout

        Keywords:
        log_name -- str, name to be displayed in logs
        log_file -- str, file for logs
        log_level -- verbosity
        """
        self.log_file = log_file
        self.log_level = log_level
        self.log_name = log_name
        self._log_init()

    @property
    def log_name(self):
        """Getter for log_name

        Returns:
        log_name -- str
        """
        return self._log_name

    @log_name.setter
    def log_name(self, log_name):
        """Title for log information
        Keyword Arguments:
        log_name -- str
        Returns:
        0 -- int
        """
        self._log_name = log_name
        return 0

    @property
    def log_file(self):
        """Getter for log_file

        Returns:
        log_file -- str
        """
        return self._log_file

    @log_file.setter
    def log_file(self, log_file):
        """Store the file name to store logs
        Keyword Arguments:
        log_file -- str
        Returns:
        0 -- int
        """
        self._log_file = log_file
        return 0

    @property
    def log_level(self):
        """Getter for log_level
        Keyword Arguments:
        Returns:
        log_level -- int
        """
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        """Store the file name to store logs
        Keyword Arguments:
        log_level -- int
        Returns:
        0 -- int
        """
        self._log_level = log_level
        return 0

    def _log_init(self):
        """Init the log engine

        If log_file is equal to None, then write the logs to
        stdout

        Keyword Arguments:
        log_file  -- filename string to store logs
        log_level -- verbosity

        Returns:
        0 -- ins
        """
        # logger instance
        self._logger = logging.getLogger(self.log_name)
        self._logger.setLevel(self.log_level)
        # log formatter
        log_strformat = '%(asctime)s %(name)s'
        log_strformat += ' (%(levelname)s) | %(message)s'
        formatter = logging.Formatter(log_strformat)

        # log handlers
        if self.log_file is None:
            # -------- console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self._logger.addHandler(ch)
        else:
            # -------- file handler
            fh = logging.FileHandler(self.log_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)
        return 0

    @property
    def logger(self):
        """Getter for Logger object
        Returns:
        logger -- logging object instance
        """
        return self._logger
