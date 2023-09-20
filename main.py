from flask import Flask, request, jsonify, render_template
import dfagent
import prompts

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/inner_page/")
def inner_page():
    return render_template('inner_page.html')

@app.route("/send-message/<message>")
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
