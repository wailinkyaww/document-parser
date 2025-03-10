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

        # Convert logger name to file-based namespacing
        record.name = self.format_namespace(record.name)

        return super().format(record)

    def format_namespace(self, logger_name: str) -> str:
        """ Convert logger name to file-based namespace (e.g., src:module:a) """
        parts = logger_name.split(".")
        return ":".join(parts) if parts else logger_name


def get_logger(file_path):
    """ Returns a logger with a namespace based on the file path. """

    project_base_path = os.path.abspath(os.path.dirname(__file__))
    relative_path = os.path.relpath(file_path, project_base_path).replace(os.sep, ".")
    module_namespace = relative_path.replace(".py", "")

    logger = logging.getLogger(module_namespace)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Apply formatting
    formatter = CustomFormatter(
        '%(asctime)s %(name)s [%(funcName)s:L%(lineno)d] %(levelname)s %(message)s %(time_taken)s')
    console_handler.setFormatter(formatter)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
