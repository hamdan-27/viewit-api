from waitress import serve
from main import app  # Assuming your Flask app instance is named 'app' and is in the 'app' module

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=3000)
