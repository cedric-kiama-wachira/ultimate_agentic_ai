import streamlit as st
from openai import OpenAI
from google import genai
from google.genai import types
from groq import Groq
from core.config import config


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

# On streamlit app lets create a sidebar with the following options:

with st.sidebar:
    st.title("Settings")

# The first is a drop down to select the model providers through streamlit:
    provider = st.selectbox("Provider", ["OpenAi", "Groq", "Google"])
    if provider == "OpenAi":
        model_name = st.selectbox("Model", ["gpt-5-nano", "gpt-5-mini"])
    elif provider =="Groq":
        model_name = st.selectbox("Model", ["openai/gpt-oss-120b"])
    else:
        model_name = st.selectbox("Model", ["gemini-3.8-flash", "gemini-3.5-flash-lite"])

# Saving the model and provider to the sessions state:

    st.session_state.provider = provider
    st.session_state.model_name = model_name


# Initializing message objects for Groq and OpenAI in our session state or object:

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello how can I assist you today?"}]

# Print all the messages in the chat session state or object:

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# This is how we define the chat box which we will add our code to: 

if prompt := st.chat_input("Hello how can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = run_llm(st.session_state.provider, st.session_state.model_name, st.session_state.messages)
        response_data = output
        answer = response_data
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    

