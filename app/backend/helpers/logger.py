import logging
import sys
import atexit
from ..helpers import Colors


class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        'DEBUG': Colors.BLUE,
        'INFO': Colors.GREEN,
        'WARNING': Colors.YELLOW,
        'ERROR': Colors.RED,
        'CRITICAL': Colors.MAGENTA,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelname, "")
        message = super().format(record)
        return f"{color}{message}{Colors.RESET}"


class Logger:
    instance = None

    @classmethod
    def get_logger(cls):
        if cls.instance is None:
            cls.instance = logging.getLogger('app')
            cls.instance.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            formatter = ColorFormatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            cls.instance.addHandler(handler)
            cls.instance.propagate = False

        return cls.instance

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(message)

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message):
        cls.get_logger().error(message)

    @classmethod
    def critical(cls, message):
        cls.get_logger().critical(message)


def cleanup_logger():
    Logger.info("Application is closing, performing cleanup.")


atexit.register(cleanup_logger)
