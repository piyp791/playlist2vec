import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import ecs_logging

HOME_PATH = os.getcwd()

class MergingLoggerAdapter(logging.LoggerAdapter):
    """LoggerAdapter that merges extras"""

    def process(self, msg, kwargs):
        kwargs["extra"] = {**(self.extra or {}), **kwargs.get("extra", {})}
        return msg, kwargs


class LogFactory:
    def __init__(self, config):
        self.config = config

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        consoleLogFormatter = logging.Formatter(
            fmt='%(asctime)s :: %(name)s :: %(levelname)-8s :: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(consoleLogFormatter)
        logger.addHandler(console_handler)
        
        log_dir = os.path.join(HOME_PATH, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = RotatingFileHandler(
        os.path.join(log_dir, self.config['logs']['filename']),
            maxBytes=self.config['logs']['max_bytes'],
            backupCount=self.config['logs']['backup_count'])

        file_handler.setFormatter(ecs_logging.StdlibFormatter())
        logger.addHandler(file_handler)
        logger = MergingLoggerAdapter(logger, {'source_application': self.config['source_application']})

        return logger
