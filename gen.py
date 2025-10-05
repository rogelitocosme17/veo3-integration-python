from google import genai
import time
from datetime import datetime
from google.genai import types
from google.genai.types import GenerateVideosOperation
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

operation_id = "models/veo-3.0-generate-001/operations/2ndklfg582ib"

operation = GenerateVideosOperation(name=operation_id)

operation = client.operations.get(operation)

print("Operation", operation)
print("Operation Status", operation.done)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"generate_video_by_veo3_{timestamp}.mp4"
filepath = f"static/{filename}"

# Download the generated video.
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save(filepath)

print("Generated video saved to dialogue_example.mp4")