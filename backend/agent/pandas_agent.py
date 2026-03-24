import os
import matplotlib.pyplot as plt

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load API Key
load_dotenv()


def create_agent(df):

    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.1-8b-instant",  # Stable model
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True
    )

    return agent