import streamlit as st
import requests  # I will use a simple request library to call the FirstAPI endpoint.
from chatbot_ui.core.config import config

# Creating a new function for calling the FirstAPI endpoint.

def api_call(method, url, **kwargs):

    def _show_error_popup(message):
        """Show error messsage as a popup in the top-right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }

    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid response format from server."}

        if response.ok:
            return True, response_data

        return False, response_data

    except requests.exceptions.ConnectionError:
        _show_error_popup("Connection error. Please check your network connection.")
        return False, {"message": "Connection error."}
    except requests.exceptions.Timeout:
        _show_error_popup("The request timed out. Please try again later.")
        return False, {"message": "Request timed out."}
    except Exception as e:
        _show_error_popup(f"An unexpected error occurred: {str(e)}")
        return False, {"message": str(e)}

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
        output = api_call("post", f"{config.API_URL}/chat", json={"provider": st.session_state.provider, "model_name": st.session_state.model_name, "messages": st.session_state.messages})
        response_data = output[1]
        answer = response_data["message"]
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

    

