# prompt-flow-ui

This repository contains an implementation of a user interface (UI) for Azure Machine Learning Prompt Flow deployments. The chat interface is developed using Streamlit.

This was primarily developed for Microsoft's "Chat with Wiki" demo but can be adapted as needed based on the input/output schema of your Prompt Flow implementation.

# Instructions:
1. Clone the repository: `git clone https://github.com/shah-zeb-naveed/prompt-flow-ui`
2. Install streamlit python package `pip install streamlit`.
3. Create a `.env` file and add your Azure Prompt Flow deployment key as: AZURE_ENDPOINT_KEY=ENTER_YOUR_KEY
3. Run the Streamlit app using `streamlit run app.py`.

# Thanks to:
- Microsoft for providing code for querying the endpoint.
- Streamlit for it's chat elements and session state features. 

# Disclaimer:
This is an unofficial implementation and is not supported by Microsoft.

*Please star this repo if you found this helpful. Thanks.*