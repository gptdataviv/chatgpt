import openai
import llama_index
import pypdf2
import json
from .creds import Creds

# Set your OpenAI API key
openai.api_key = Creds.get_key('GPT')

# Define the input and output paths for training data and JSON file
input_path = "training_data/"
output_path = "training_data.json"

# Initialize the llama indexer
indexer = llama_index.Indexer()

# Process and index the training data
for filename in os.listdir(input_path):
    if filename.endswith(".txt"):
        with open(os.path.join(input_path, filename), "r") as f:
            text = f.read()
        indexer.add_text(text)

    elif filename.endswith(".pdf"):
        with open(os.path.join(input_path, filename), "rb") as f:
            pdf_reader = pypdf2.PdfReader(f)
            for page in pdf_reader.pages:
                text = page.extract_text()
                indexer.add_text(text)

# Generate the JSON file for training
with open(output_path, "w") as f:
    json.dump(indexer.get_json(), f)