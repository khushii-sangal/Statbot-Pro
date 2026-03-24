import os
import matplotlib.pyplot as plt

from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def create_agent(df):

    llm = ChatGroq(
        temperature=0,
        model_name="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    prefix = """
    You are a smart data analyst.

    - Use pandas for calculations
    - Use matplotlib for charts

    IMPORTANT RULES:
    - If user asks about trends, comparisons, distribution → create a graph
    - If user uses words like plot, graph, chart, visualize → create graph

    GRAPH RULES:
    - Use matplotlib
    - Save graph using:
    plt.savefig("static/chart.png")
    - Do NOT use plt.show()
    - Always call plt.close()

    Always use dataframe 'df'.
    """

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        prefix=prefix,
        allow_dangerous_code=True
    )

    return agent