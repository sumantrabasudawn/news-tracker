import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a 50-word intelligence brief on India's energy transition."
)

print("\n")
print(response.output_text)
print("\n✅ GPT API WORKING")