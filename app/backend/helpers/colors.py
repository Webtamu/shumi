class Colors():
    RESET = "\033[0m"
    YELLOW = "\033[33m"
    BRIGHT_YELLOW = "\033[93m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"

    def __str__(self):
        return self.value
