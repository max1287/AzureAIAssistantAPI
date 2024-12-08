import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AzureOpenAI
from openai.types.beta import Thread
from openai.types.beta import Assistant

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),  # Your API key for the assistant api model
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),  # API version  (i.e. 2024-02-15-preview)
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)