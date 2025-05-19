import logging
import sys
import atexit
from ..helpers import Colors


class Logger:
    instance = None

    @classmethod
    def get_logger(cls):
        if cls.instance is None:
            # Create singleton logger
            cls.instance = logging.getLogger('app')
            cls.instance.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)

            cls.instance.addHandler(handler)
            cls.instance.propagate = False

        return cls.instance

    @classmethod
    def debug(cls, message):
        """Log a blue debug message."""
        if cls.get_logger():
            cls.get_logger().debug(f"{Colors.BLUE}{message}{Colors.RESET}")

    @classmethod
    def info(cls, message):
        """Log a green info message."""
        if cls.get_logger():
            cls.get_logger().info(f"{Colors.GREEN}{message}{Colors.RESET}")

    @classmethod
    def warning(cls, message):
        """Log a yellow warning message."""
        if cls.get_logger():
            cls.get_logger().warning(f"{Colors.YELLOW}{message}{Colors.RESET}")

    @classmethod
    def error(cls, message):
        """Log a red error message."""
        if cls.get_logger():
            cls.get_logger().error(f"{Colors.RED}{message}{Colors.RESET}")

    @classmethod
    def critical(cls, message):
        """Log a magenta critical message."""
        if cls.get_logger():
            cls.get_logger().critical(f"{Colors.MAGENTA}{message}{Colors.RESET}")


# Registering cleanup method using atexit
def cleanup_logger():
    logger = Logger.get_logger()
    if logger:
        Logger.info("Application is closing, performing cleanup.")


# Register the cleanup function for safe logging during application shutdown
atexit.register(cleanup_logger)
