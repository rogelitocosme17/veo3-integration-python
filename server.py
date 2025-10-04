from google import genai
import time
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

        # Download the generated video.
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save("/static/dialogue_example.mp4")

        # Return URL for frontend
        return {"video_url": f"http://127.0.0.1:9000/static/dialogue_example.mp4"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





