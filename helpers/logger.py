import logging
import sys

from helpers.helpers import Colors


class Logger:
    _logger = None

    @classmethod
    def _get_logger(cls):
        """Get or initialize the logger instance."""
        if cls._logger is None:
            # Create logger
            cls._logger = logging.getLogger('app')
            cls._logger.setLevel(logging.DEBUG)

            # Create console handler with a formatter
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            cls._logger.addHandler(handler)

            # Prevent log propagation to avoid duplicate logs
            cls._logger.propagate = False

        return cls._logger

    def __str__(self):
        return self.value

    @classmethod
    def debug(cls, message):
        """Log a blue debug message."""
        cls._get_logger().debug(f"{Colors.BLUE}{message}{Colors.RESET}")

    @classmethod
    def info(cls, message):
        """Log a green info message."""
        cls._get_logger().info(f"{Colors.GREEN}{message}{Colors.RESET}")

    @classmethod
    def warning(cls, message):
        """Log a yellow warning message."""
        cls._get_logger().warning(f"{Colors.YELLOW}{message}{Colors.RESET}")

    @classmethod
    def error(cls, message):
        """Log a red error message."""
        cls._get_logger().error(f"{Colors.RED}{message}{Colors.RESET}")

    @classmethod
    def critical(cls, message):
        """Log a magenta critical message."""
        cls._get_logger().critical(f"{Colors.MAGENTA}{message}{Colors.RESET}")
