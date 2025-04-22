import sys
from app import App

if __name__ == "__main__":
    app = App(sys.argv)
    app_instance = app
    sys.exit(app.exec())
