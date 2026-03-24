from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from agent.pandas_agent import create_agent

app = FastAPI()

# Enable CORS (important for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create folders
os.makedirs("data", exist_ok=True)
os.makedirs("static", exist_ok=True)


@app.get("/")
def home():
    return {"message": "Statbot-Pro Backend Running 🚀"}

uploaded_file_path = None  # global variable


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global uploaded_file_path

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    uploaded_file_path = file_path  # save path

    return {"message": "File uploaded successfully", "filename": file.filename}


@app.post("/ask/")
async def ask_question(question: str):
    global uploaded_file_path

    try:
        if uploaded_file_path is None:
            return {"error": "Please upload a CSV file first"}

        df = pd.read_csv(uploaded_file_path)

        agent = create_agent(df)

        response = agent.run(question)

        return {"response": str(response)}

    except Exception as e:
        return {"error": str(e)}