# import uvicorn
# from main import app
# # import sys
# # from gunicorn.app.wsgiapp import run


# if __name__ == "__main__":
#     # sys.argv = "gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:5000".split()
#     # sys.exit(run())
#     uvicorn.run(app, host="0.0.0.0", port=8181)

from gunicorn.app.base import BaseApplication
from uvicorn.workers import UvicornWorker
from main import app  # Import your FastAPI app instance

class CustomGunicornApp(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        'bind': '0.0.0.0:8000',  # Set the host and port
        'workers': 4,  # Number of worker processes
        'worker_class': 'uvicorn.workers.UvicornWorker',  # Use Uvicorn worker
    }

    custom_gunicorn_app = CustomGunicornApp(app, options)
    custom_gunicorn_app.run()
