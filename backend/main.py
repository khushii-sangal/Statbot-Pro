import os
from dotenv import load_dotenv
load_dotenv()
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



# Import your agent
from agent.pandas_agent import create_agent

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# ✅ Allow frontend (React) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to store uploaded CSV
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

agent = None


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    global agent

    try:
        # Save file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("✅ File saved at:", file_path)

        # Create agent
        agent = create_agent(file_path)

        print("✅ Agent created successfully")

        return {"message": "File uploaded successfully!"}

    except Exception as e:
        print("❌ ERROR during upload:", str(e))
        return {"error": str(e)}

from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

@app.post("/ask/")
async def ask_question(request: QueryRequest):
    global agent

    try:
        if agent is None:
            return {"error": "Please upload a CSV first."}

        response = agent.run(request.query)

        return {"response": response}

    except Exception as e:
        return {"error": str(e)}