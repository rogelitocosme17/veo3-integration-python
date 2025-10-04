import google.generativeai as genai

# Replace with your actual API key
client = genai.Client(api_key="...")

prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

print(f"Client Type: {type(client)}")
print(f"Client Attributes: {vars(client)}")
