from fastapi import FastAPI, UploadFile, File, Query
from services.file_service import load_csv
from agent.pandas_agent import create_agent
from dotenv import load_dotenv
load_dotenv()

import os

api_key = os.getenv("GROQ_API_KEY")
app = FastAPI()

# Temporary storage (we'll improve later)
df_store = {}

@app.get("/")
def home():
    return {"message": "CSV AI Agent Running 🚀"}

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    df, error = load_csv(file)

    if error:
        return {"error": error}

    file_id = file.filename
    df_store[file_id] = df

    return {
        "message": "File uploaded successfully",
        "file_id": file_id,
        "columns": list(df.columns),
        "rows": len(df)
    }

@app.get("/ask/")
def ask_question(file_id: str = Query(...), query: str = Query(...)):
    
    if file_id not in df_store:
        return {"error": "Invalid file_id. Upload file first."}

    df = df_store[file_id]

    try:
        agent = create_agent(df)
        result = agent.run(query)

        return {"answer": result}

    except Exception as e:
        return {"error": str(e)}