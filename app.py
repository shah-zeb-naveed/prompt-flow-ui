import streamlit as st
import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AZURE_ENDPOINT_KEY = os.environ['AZURE_ENDPOINT_KEY']

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on the client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def main():
    

    allowSelfSignedHttps(True)

    st.title("Azure Prompt Flow Chat Interface")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for interaction in st.session_state.chat_history:
        if interaction["inputs"]["question"]:
            with st.chat_message("user"):
                st.write(interaction["inputs"]["question"])
        if interaction["outputs"]["answer"]:
            with st.chat_message("assistant"):
                st.write(interaction["outputs"]["answer"])

    # React to user input
    if user_input := st.chat_input("Ask me anything..."):

        # Display user message in chat message container
        st.chat_message("user").markdown(user_input)
        

        # Query API
        data = {"chat_history": st.session_state.chat_history, 'question' : user_input}
        body = json.dumps(data).encode('utf-8')
        url = 'https://shahml-hhrub.eastus.inference.ml.azure.com/score'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {AZURE_ENDPOINT_KEY}',
            'azureml-model-deployment': 'shahml-hhrub-1'
        }
        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            response_data = json.loads(response.read().decode('utf-8'))

            # render
            with st.chat_message("assistant"):
                st.markdown(response_data['answer']) 

            # add user input to chat history
            st.session_state.chat_history.append(
                {"inputs": {"question": user_input},
                 "outputs": {"answer": response_data['answer']}}
            )

        except urllib.error.HTTPError as error:
            st.error(f"The request failed with status code: {error.code}")
            st.text(error.read().decode("utf8", 'ignore'))

if __name__ == "__main__":
    main()
