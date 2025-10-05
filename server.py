from google import genai
import time
from datetime import datetime
from google.genai import types
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the GenAI client
client = genai.Client(api_key=google_api_key)

# Initialize FastAPI app
app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # your Next.js frontend
        "http://127.0.0.1:3000",   # sometimes the browser switches to 127.0.0.1
    ],
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define request model
class PromptRequest(BaseModel):
    prompt: str

# Initial prompt
prompt = """A cute creature with snow leopard-like fur is walking in winter forest, 3D cartoon style render."""

# Endpoint to generate video
@app.post("/generate")
def generate(req: PromptRequest):
    try:        
        operation = client.models.generate_videos(
            model="veo-3.0-generate-001",
            prompt=prompt,
        )
        
        # Poll the operation status until the video is ready.
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            operation = client.operations.get(operation)

        return {"operation_id": operation.name}
    
        # # Prepare unique filename with timestamp
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f"generate_video_by_veo3_{timestamp}.mp4"
        # filepath = f"static/{filename}"

        # # Download the generated video.
        # generated_video = operation.response.generated_videos[0]
        # client.files.download(file=generated_video.video)
        # generated_video.video.save(filepath)

        # # Return URL for frontend
        # return {"video_url": f"http://127.0.0.1:9000/static/{filename}"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Check the status of video generation
@app.get("/check/{operation_id}")
def check_status(operation_id: str):
    try:
        operation = client.operations.get(operation_id)
        if operation.done:
            return {"status": "done"}
        else:
            return {"status": "in_progress"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{operation_id}")
def download_video(operation_id: str):
    try:
        operation = client.operations.get(operation_id)
        if not operation.done:
            raise HTTPException(status_code=400, detail="Operation is still in progress.")
        
        # Prepare unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generate_video_by_veo3_{timestamp}.mp4"
        filepath = f"static/{filename}"

        # Download the generated video.
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(filepath)

        # Return URL for frontend
        return {"video_url": f"http://127.0.0.1:9000/static/{filename}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
