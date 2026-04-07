import os
import pandas as pd
import matplotlib.pyplot as plt
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq


def create_agent(csv_path):
    try:
        # 📂 Load CSV
        print("📂 Loading CSV...")
        df = pd.read_csv(csv_path)
        print("✅ CSV Loaded:", df.shape)

        # 🔑 Load API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Check your .env file")

        print("🔑 API Key Loaded")

        # 🤖 Use WORKING Groq model
        llm = ChatGroq(
            api_key=api_key,
            model="llama-3.1-8b-instant"   # ✅ latest working model
        )

        print("🤖 LLM Initialized")

        # 🧠 Create Pandas Agent
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            allow_dangerous_code=True
        )

        print("✅ Agent Ready")

        # ✅ Clean wrapper class (no self errors)
        class AgentWrapper:
            def run(self, query):
                try:
                    print("💬 Query:", query)

                    # 📊 Graph handling
                    if "plot" in query.lower() or "graph" in query.lower():
                        df.plot(kind="bar")
                        os.makedirs("static", exist_ok=True)
                        plt.savefig("static/chart.png")
                        plt.close()

                        return {"graph": True}

                    # 🧠 Normal query
                    result = agent.run(query)
                    return result

                except Exception as e:
                    print("❌ Query Error:", str(e))
                    return f"Error: {str(e)}"

        return AgentWrapper()

    except Exception as e:
        print("❌ AGENT CREATION ERROR:", str(e))
        raise e