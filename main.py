from flask import Flask, request, jsonify, send_from_directory
import dfagent
import prompts

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def hello():
    return jsonify({
        "message": "Welcome to the Viewit API! Please navigate to the /chat endpoint" \
           " followed by your input to use the API."}), 200


@app.route("/chat/<message>")
def send_message(message):

    temperature = request.args.get('temperature')
    model = request.args.get('model')

    # AGENT CREATION HAPPENS HERE
    agent = dfagent.create_pandas_dataframe_agent(
        model=model or dfagent.model,
        temperature=temperature or dfagent.TEMPERATURE,
        df=dfagent.df,
        prefix=prompts.REIDIN_PREFIX,
        suffix=prompts.SUFFIX,
        format_instructions=prompts.FORMAT_INSTRUCTIONS,
        verbose=True,
        handle_parsing_errors=True,
        # max_execution_time=30,
    )

    response = agent.run(message)
    response_data = {
        'messages': {
            "role": "assistant",
            "content": response
        },
        'model': model or dfagent.model,
        'temperature': (float(temperature) if temperature else "") or dfagent.TEMPERATURE
    }

    return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=True)
