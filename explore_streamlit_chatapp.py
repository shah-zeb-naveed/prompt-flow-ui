import streamlit as st
import random
import time
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AZURE_KEY = os.environ['OPENAI_KEY']

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=AZURE_KEY)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) # st.write() also works fine!

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Bot's response
    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # immediate render
        #st.markdown(response) 

        # streaming render dummy
        #stream = response_generator()

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        response = st.write_stream(stream)


    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})