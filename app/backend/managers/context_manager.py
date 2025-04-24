class ContextManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ContextManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.user_id = None
            self.username = None
            self.email = None
