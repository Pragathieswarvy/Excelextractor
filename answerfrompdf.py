import streamlit as st
import pandas as pd
import requests
import json
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your API key
apiKey = "4c2f8a2c-6149-4877-b61f-c5f0af99a2d7"

def apiFunction(usersInputObj):
    # Define input fields
    inputsArray = [
        {"id": "{input_1}", "label": "Enter query", "type": "text"},
        {"id": "{input_2}", "label": "Upload an Excel file", "type": "file"}
    ]

    # Construct the prompt
    prompt = "Extract the data related to the question {input_1} from this Excel file url {input_2}"
    filesData = {}
    textData = {}

    for inputObj in inputsArray:
        inputId = inputObj['id']
        if inputObj['type'] == 'text':
            prompt = prompt.replace(inputId, usersInputObj.get(inputId, ""))
        elif inputObj['type'] == 'file':
            if inputId in usersInputObj:
                file = usersInputObj[inputId]
                if file and file.name.endswith('.xlsx'):  # Check file type
                    filesData[inputId] = (file.name, file)
                else:
                    return "Error: The file type is not supported. Please upload an `.xlsx` file."

    textData['details'] = json.dumps({
        'appname': 'Excel data extractor',
        'prompt': prompt,
        'documentId': 'no-embd-type',
        'appId': '66c8ae9c64d827b744a2a136',
        'memoryId': '',
        'apiKey': apiKey
    })

    try:
        # Ensure you're using the correct URL and HTTP method
        response = requests.post('https://apiappstore.guvi.ai/api/output', data=textData, files=filesData)
        response.raise_for_status()  # Raise an error for bad responses

        output = response.json()
        return output.get('output', 'No output found.')
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return f"Request failed: {e}"

# Streamlit app
def main():
    st.title("Excel Data Extractor")

    # User input
    query = st.text_input("Enter your query")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if st.button("Submit"):
        if query and uploaded_file:
            usersInputObj = {
                '{input_1}': query,
                '{input_2}': uploaded_file  # Streamlit file uploader returns a file-like object
            }

            output = apiFunction(usersInputObj)
            url_regex = r'http://localhost:7000/'
            replaced_string = re.sub(url_regex, 'https://apiappstore.guvi.ai/', output)
            st.write(replaced_string)
        else:
            st.error("Please enter a query and upload an Excel file.")

if __name__ == "__main__":
    main()





