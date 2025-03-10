import logging
import os
from datetime import datetime, timezone


class CustomFormatter(logging.Formatter):
    last_log_time = None  # Maintain state across logs

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    def format(self, record: logging.LogRecord) -> str:
        if CustomFormatter.last_log_time is not None:
            time_taken = record.created - CustomFormatter.last_log_time
            record.time_taken = f"+{time_taken * 1000:.0f}ms" if time_taken < 1 else f"+{time_taken:.3f}s"
        else:
            record.time_taken = ""

        CustomFormatter.last_log_time = record.created

        return super().format(record)


def get_logger(file_path):
    """
    Returns a logger with a namespace based on the file path.

    Sample usage:
    logger = get_logger(__file__)
    logger.info('log statement here')
    """

    base_dir = 'src'

    current_file_path = os.path.abspath(os.path.dirname(__file__))
    project_base_path = os.path.join(current_file_path, '..')

    namespace = (base_dir + '/' + os.path.relpath(file_path, project_base_path)).replace(os.sep, ":")

    logger = logging.getLogger(namespace)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Apply formatting
    formatter = CustomFormatter(
        '%(name)s [%(funcName)s:L%(lineno)d] %(levelname)s %(message)s %(time_taken)s')
    console_handler.setFormatter(formatter)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
