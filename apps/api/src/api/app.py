# Importring some stuff
# FirstApi itself and Pydantic which will be used to define the 
# structure and schema of the  data objects
# FirstApi used pydantic data classes alot  
# Schemma via FastAPi requests and responses are defined using pydantic data classes.

from fastapi import FastAPI,Request
from pydantic import BaseModel

# Some LLM CLients

from openai import OpenAI
from groq import Groq
from google import genai
from google.genai import types

# The config file

from api.core.config import config

# Configuring our initial logger.

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__) 

# Implementing the RUN_LLM function from earlier - so I copied the one from the src/app.py file.

def run_llm(provider, model_name, messages, max_tokens=500):

    if provider == "OpenAi":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
    elif provider == "Groq":
        client = Groq(api_key=config.GROQ_API_KEY)
    else:
        client = genai.Client(api_key=config.GOOGLE_API_KEY)

    if provider == "Google":
        return client.models.generate_content(
            model=model_name,
            # Initializing message objects for Google and extracting 
            # the content of the messages:
            contents=[message["content"] for message in messages],
            config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="low")),
        ).text
    elif provider == "Groq":
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
            reasoning_effort="low",
        ).choices[0].message.content
    else:
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
            reasoning_effort="minimal"
        ).choices[0].message.content

# Definining our pydantic model as a class

class ChatRequest(BaseModel):
    provider: str
    model_name: str
    messages: list[dict]

class ChatResponse(BaseModel):
    message: str


# Initializing my firstApi application

app = FastAPI()

# Using the app decorator to decorate the function, 
# and that function will be invoked when we place a request to a specific endpoint.
# 

@app.post("/chat")
def chat(
    request: Request,
    payload: ChatRequest
) -> ChatResponse:

    result = run_llm(payload.provider, payload.model_name, payload.messages)

    return ChatResponse(message=result)

