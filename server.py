import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv = "gunicorn --bind 0.0.0.0:5151 main:app".split()
    sys.exit(run())

# from waitress import serve
# from main import app  # Assuming your Flask app instance is named 'app' and is in the 'app' module

# if __name__ == "__main__":
#     serve(app)
