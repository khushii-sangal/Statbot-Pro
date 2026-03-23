from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
import os
def create_agent(df):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",   # fast + free model
        api_key = os.getenv("GROQ_API_KEY")
    )

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True
    )

    return agent