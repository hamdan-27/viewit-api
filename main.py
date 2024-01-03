from flask import Flask, request, jsonify, send_from_directory
# from flask_swagger_ui import get_swaggerui_blueprint
from langchain.callbacks import get_openai_callback
from openai import OpenAI
import dfagent
import prompts
import os

app = Flask(__name__)


# @app.route("/static/<path:path>")
# def send_static(path):
#     return send_from_directory("static", path)

# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': 'Viewit AI API'
#     }
# )
# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/")
def hello():
    return jsonify({
        "message": "Welcome to the Viewit API! Please navigate to the /chat endpoint" \
           " for the chatbot API, or the /description endpoint for the property" \
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



@app.route("/description", methods=["POST"])
def generate():
    try:
        client = OpenAI()
        payload = request.get_json()
        features = payload.get("features", {})
        model = request.args.get('model')
        temp = request.args.get('temperature')
        temperature = float(temp) if temp else None
        seo = payload.get("seo")
        seo_list = seo.replace(' ', '').split(',') if seo else None

        seo_prompt = f"Use these keywords in your description for better SEO: {seo_list}\n" if seo else ''

        prompt = f"""Generate ONLY the description for a property listing in under 1000 \
        characters. The features of the property are mentioned in the json provided by the user. \
        The price should be in AED.
        {seo_prompt}
        """

        completion = client.chat.completions.create(
            model= model or "gpt-4-1106-preview",
            temperature=temperature or 0.1,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"{features}"}
            ]
        )

        description = completion.choices[0].message.content

        response_data = {
            "response": {
                "description": description
            },
            "model": model or "gpt-4-1106-preview",
            "temperature": temperature or 0.1
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
