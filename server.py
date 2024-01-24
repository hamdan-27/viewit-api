import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


# import sys
# from gunicorn.app.wsgiapp import run

# if __name__ == "__main__":
#     sys.argv = "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5151".split()
#     sys.exit(run())


# from hypercorn import run
# from main import app

# if __name__ == '__main__':
#     run(app)