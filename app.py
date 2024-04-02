import streamlit as st
import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
AZURE_KEY = os.environ['AZURE_ENDPOINT']

# #for proxy_env in ['http_proxy', 'https_proxy']
# os.environ['https_proxy'] = ''
# os.environ['http_proxy'] = ''


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on the client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def main():
    st.title("Azure Prompt Flow Chat Interface")

    allowSelfSignedHttps(True)  # this line is needed if you use a self-signed certificate in your scoring service.

    # Initialize chat history
    chat_history = st.session_state.get("chat_history", [])

    # Display chat history
    for interaction in chat_history:
        if interaction["inputs"]["question"]:
            with st.chat_message("user"):
                st.write(interaction["inputs"]["question"])
        if interaction["outputs"]["answer"]:
            with st.chat_message("assistant"):
                st.write(interaction["outputs"]["answer"])

    # Display user input box at the bottom of the screen
    user_input = st.chat_input("Say something")

    if user_input:
        # Add user input to chat history
        chat_history.append({"inputs": {"question": user_input}, "outputs": {"answer": ""}})

        # Define data
        data = {"chat_history": chat_history}

        body = json.dumps(data).encode('utf-8')

        url = 'https://shahml-hhrub.eastus.inference.ml.azure.com/score'
        api_key = AZURE_KEY

        # Set up request headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'azureml-model-deployment': 'shahml-hhrub-1' }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read().decode('utf-8')
            response_data = json.loads(result)

            # Extract bot response from the API response
            bot_response = response_data['answer']

            # Add bot response to chat history
            chat_history[-1]["outputs"]["answer"] = bot_response

            # Update session state
            st.session_state.chat_history = chat_history

        except urllib.error.HTTPError as error:
            st.error(f"The request failed with status code: {error.code}")
            st.text(error.read().decode("utf8", 'ignore'))

if __name__ == "__main__":
    main()
