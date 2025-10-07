from google import genai
import time
from google.genai import types
from dotenv import load_dotenv
import os
from PIL import Image

# Load the .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the GenAI client
client = genai.Client(api_key=google_api_key)

# prompt = """A cute creature with snow leopard-like fur is walking in winter forest, 3D cartoon style render."""
prompt = """Bunny runs away."""

image_path = os.path.join("images", "base.png")

# Create a types.Image from local file
with open(image_path, "rb") as f:
    base_image_bytes = f.read()

base_image = types.Image(
    image_bytes=base_image_bytes,
    mime_type="image/png"
)

operation = client.models.generate_videos(
    model="veo-3.0-generate-001",
    prompt=prompt,
    image=base_image
)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation to complete...")
    time.sleep(10)
    operation = client.operations.get(operation)

print("Operation", vars(operation))
print("Operation Name", operation.name)
print("Operation Done", operation.done)
print("Operation Metadata", operation.metadata)

operation_id = operation.response.generated_videos[0].video.uri
print(f"Operation ID: {operation_id}")

print("Video generation Result:", vars(operation.result))
print("Video generation Response:", vars(operation.response))

# Download the generated video.
generated_video = operation.response.generated_videos[0]
print("Generated Video", vars(generated_video))

client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("Generated video saved to dialogue_example.mp4")
