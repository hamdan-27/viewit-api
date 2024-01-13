from fastapi import FastAPI, HTTPException, Request, Query, Body
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from langchain.callbacks import get_openai_callback
from openai import OpenAI

from agents import model, df, TEMPERATURE, create_pandas_dataframe_agent
import prompts


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

client = OpenAI()

agent = create_pandas_dataframe_agent(
    model=model,
    temperature=TEMPERATURE,
    df=df,
    prefix=prompts.REIDIN_PREFIX,
    suffix=prompts.SUFFIX,
    format_instructions=prompts.FORMAT_INSTRUCTIONS,
    verbose=True,
    handle_parsing_errors=True
)


@app.get(
        "/", 
        # response_class=HTMLResponse
        )
def hello(
    # request: Request
    ):
    # return templates.TemplateResponse('index.html.jinja', {"request": request})

    return {"message": "Welcome to the Viewit API! Please navigate to the /chat endpoint"
            " for the chatbot API, or the /description endpoint for the property"
            " description API."}


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")


@app.get("/chat/{message}")
def send_message(message: str):
    try:
        with get_openai_callback() as cb:
            response = agent.run(message)
            print("\n", cb,"\n")

        response_data = {
            'messages': {
                "role": "assistant",
                "content": response
            },
            'model': model,
            'temperature': TEMPERATURE,
            'total_tokens': str(cb.total_tokens),
            'total_cost_usd': f"{cb.total_cost:5f}"
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/description")
def generate(
    features: dict = Body(...),
    model: str = Query(default="gpt-4-1106-preview"),
    temperature: float = Query(default=0.1),
    seo: str = Body(default=None)
):
    try:
        seo_list = seo.replace(' ', '').split(',') if seo else None
        seo_prompt = f"Use these keywords in your description for better SEO: {seo_list}\n" if seo else ''

        prompt = f"""Generate ONLY the description for a property listing in under 1000 \
        characters. The features of the property are mentioned in the json provided by the user. \
        The price should be in AED.
        {seo_prompt}
        """

        completion = client.chat.completions.create(
            model=model,# or "gpt-4-1106-preview",
            temperature=temperature,# or 0.1,
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
            "model": model,# or "gpt-4-1106-preview",
            "temperature": temperature# or 0.1
        }

        return response_data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))