import os
import pandas as pd

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from agent.pandas_agent import create_agent

app = FastAPI()

# ✅ Allow CORS (important for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Folder setup
UPLOAD_FOLDER = "data"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# ✅ Serve static files (for graphs)
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

# ✅ Store uploaded file path
uploaded_file_path = None


# 🚀 Root API
@app.get("/")
def home():
    return {"message": "Statbot-Pro API is running 🚀"}


# 📂 Upload CSV
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global uploaded_file_path

    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        uploaded_file_path = file_path

        return {
            "message": "File uploaded successfully",
            "file_path": file_path
        }

    except Exception as e:
        return {"error": str(e)}


# 🤖 Ask Question
@app.post("/ask/")
async def ask_question(question: str):
    global uploaded_file_path

    try:
        if uploaded_file_path is None:
            return {"error": "Please upload a CSV file first"}

        # Load CSV
        df = pd.read_csv(uploaded_file_path)

        # Create agent
        agent = create_agent(df)

        # Run query
        response = agent.run(question)

        # Check if graph created
        graph_path = os.path.join(STATIC_FOLDER, "chart.png")

        if os.path.exists(graph_path):
            return {
                "response": str(response),
                "graph_url": "http://127.0.0.1:8000/static/chart.png"
            }

        return {"response": str(response)}

    except Exception as e:
        return {"error": str(e)}