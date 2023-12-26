from prompts import *

import os
import pandas as pd

from langchain.chains.llm import LLMChain
from langchain.tools import GooglePlacesTool
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain.agents import ZeroShotAgent, AgentExecutor
# from langchain.agents import create_pandas_dataframe_agent


def load_data(filename) -> pd.DataFrame:
    df = pd.read_csv(f"data/{filename}")
    df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y", dayfirst=True)

    return df


pd.set_option('display.max_columns', None)


def create_pandas_dataframe_agent(
        model,
        temperature,
        df: pd.DataFrame,
        prefix: str,
        suffix: str,
        format_instructions: str,
        verbose: bool,
        **kwargs) -> AgentExecutor:
    """Construct a pandas agent from an LLM and dataframe.

    Parameters:
    - model: The LLM to use.
    - temperature: The temperature of the model.
    - df: The dataframe to use as knowledge base.
    - prefix: Prefix of the prompt.
    - suffix: Suffix of the prompt.
    - format_instructions: The format to be followed by the agent.
    - verbose: Whether to display the chain of thought.
    - **kwargs: 

    Returns:
    - An AgentExecutor object
    """

    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected pandas object, got {type(df)}")

    input_variables = ["df", "input", "chat_history", "agent_scratchpad"]

    # Set up memory
    memory = ConversationBufferMemory(memory_key="chat_history")

    tools = [PythonAstREPLTool(locals={"df": df}), GooglePlacesTool()]

    prompt = ZeroShotAgent.create_prompt(
        tools=tools,
        prefix=prefix,
        suffix=suffix,
        format_instructions=format_instructions,
        input_variables=input_variables
    )
    partial_prompt = prompt.partial(df=str(df.head()))

    llm_chain = LLMChain(
        llm=ChatOpenAI(
            temperature=temperature,
            model_name=model,
            openai_api_key=os.environ['OPENAI_API_KEY']
        ),
        prompt=partial_prompt
    )
    tool_names = [tool.name for tool in tools]

    agent = ZeroShotAgent(llm_chain=llm_chain,
                          allowed_tools=tool_names, verbose=verbose)

    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=verbose,
        memory=memory,
        **kwargs
    )


# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history")


# VARIABLES
TEMPERATURE = 0.1
df = load_data('reidin_new.csv')
model = 'gpt-4'

llm = ChatOpenAI(temperature=TEMPERATURE,
                 model_name=model,
                 openai_api_key=os.environ['OPENAI_API_KEY'])

# llm = OpenAI(temperature=TEMPERATURE,
#                 model_name=MODEL_NAME,
#                 openai_api_key=st.secrets['api_key'])


# API keys
