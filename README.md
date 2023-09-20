# ViewIT API

## How to use

### 1. Clone repository to your local machine
    
    git clone https://github.com/hamdan-27/viewit-api.git

### 2. Run `main.py`
Navigate to your working directory in the terminal and run `py main.py` or `py3 main.py` if you're on MacOS.

### 3. Your local server should now be live (most probably on port 5000)
Go to `localhost:5000` or `127.0.0.1:5000` on your browser

### 4. API
Use the API by navigating to the `send-message/` endpoint of the url and enter your message.

_Example:_ 

    https://localhost:5000/send-message/how many units are available

#### Query Parameters
You can also specify the temperature you want the model to be in, using the `temperature` query parameter. The default is 0.1

_Example:_ 

    https://localhost:5000/send-message/how many units are available?temperature=0.3