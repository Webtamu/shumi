import sys
from app import App  

if __name__ == "__main__":
    app = App(sys.argv)
    theApp = app 
    sys.exit(app.exec())  