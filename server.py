# import uvicorn
# from main import app
import sys
from gunicorn.app.wsgiapp import run


if __name__ == "__main__":
    sys.argv = "sudo gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80".split()
    sys.exit(run())
    # uvicorn.run(app, host="0.0.0.0", port=8181)