import logging
import sys

from ..helpers import Colors


class Logger:
    instance = None

    @classmethod
    def get_logger(self):
        if self.instance is None:
            # Create singleton logger
            self.instance = logging.getLogger('app')
            self.instance.setLevel(logging.DEBUG)

            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)

            self.instance.addHandler(handler)
            self.instance.propagate = False

        return self.instance

    def __str__(self):
        return self.value

    @classmethod
    def debug(self, message):
        """Log a blue debug message."""
        self.get_logger().debug(f"{Colors.BLUE}{message}{Colors.RESET}")

    @classmethod
    def info(self, message):
        """Log a green info message."""
        self.get_logger().info(f"{Colors.GREEN}{message}{Colors.RESET}")

    @classmethod
    def warning(self, message):
        """Log a yellow warning message."""
        self.get_logger().warning(f"{Colors.YELLOW}{message}{Colors.RESET}")

    @classmethod
    def error(self, message):
        """Log a red error message."""
        self.get_logger().error(f"{Colors.RED}{message}{Colors.RESET}")

    @classmethod
    def critical(self, message):
        """Log a magenta critical message."""
        self.get_logger().critical(f"{Colors.MAGENTA}{message}{Colors.RESET}")
