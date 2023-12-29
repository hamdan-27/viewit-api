import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv = "gunicorn --bind 0.0.0.0:3000 main:app".split()
    sys.exit(run())