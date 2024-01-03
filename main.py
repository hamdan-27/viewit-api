from langchain.callbacks import get_openai_callback
from flask import Flask, request, jsonify
from openai import OpenAI
import dfagent
import prompts
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({
        "message": "Welcome to the Viewit API! Please navigate to the /chat endpoint" \
           " for the chatbot API, or the /generate endpoint for the property" \
            " description API."}), 200


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route("/chat/<message>")
def send_message(message):

    try:
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
        
        with get_openai_callback() as cb:
            response = agent.run(message)
            print(cb)

        response_data = {
            'messages': {
                "role": "assistant",
                "content": response
            },
            'model': model or dfagent.model,
            'temperature': (float(temperature) if temperature else "") or dfagent.TEMPERATURE,
            'total_tokens': str(cb.total_tokens),
            'total_cost_usd': str(cb.total_cost)
        }

        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
