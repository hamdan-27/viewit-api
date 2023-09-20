from flask import Flask, request, jsonify, render_template
import dfagent
import prompts
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/inner_page/")
def inner_page():
    return render_template('inner_page.html')

@app.route("/send-message/<message>")
def send_message(user_data):
    
    if user_data.role != 'user':
        return jsonify({'error': 'invalid role selected.'})
    else:
        user_input = str(user_data.content)

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

    response = agent.run(user_input)
    response_data = {
        'messages': {
            "role": "assistant",
            "content": response
        },
        'model': model or dfagent.model,
        'temperature': (float(temperature) if temperature else "") or dfagent.TEMPERATURE
    }

    return jsonify(response_data), 200
# @app.route("/agent", methods=["POST"])
# def agent():
#     """The agent API endpoint."""

#     temperature = ""
#     model = ""

#     # AGENT CREATION HAPPENS HERE
#     agent = dfagent.create_pandas_dataframe_agent(
#         model=model or dfagent.model,
#         temperature=temperature or dfagent.TEMPERATURE,
#         df=dfagent.df,
#         prefix=prompts.REIDIN_PREFIX,
#         suffix=prompts.SUFFIX,
#         format_instructions=prompts.FORMAT_INSTRUCTIONS,
#         verbose=True,
#         handle_parsing_errors=True,
#         # max_execution_time=30,
#     )

#     # Get the instruction from the request body
#     instruction = request.json["instruction"]

#     # Generate a response using the agent executor
#     response = agent.run(instruction)

#     # Return the response as JSON
#     response_data = {
#         'messages': {
#             "role": "assistant",
#             "content": response
#         },
#         'model': model or dfagent.model,
#         'temperature': temperature or dfagent.TEMPERATURE
#     }

#     return jsonify(response_data), 200



if __name__ == "__main__":
    app.run(debug=True)
