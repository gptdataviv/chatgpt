import openai
import json

# preprocessing training data .py file will create a JSON file of the training data set
# That file will be used here to train our own custom GPT Model
# Load the JSON file containing the training data
with open("training_data.json", "r") as f:
    training_data = json.load(f)

# Train the chatbot using the OpenAI API
response = openai.Model("gpt-chat", params={"prompt": training_data}).generate()
# Response
chatbot_model = response["data"]["model"]

# Prompt the chatbot with a conversation starter
prompt = "Hello, how can I help you today?"

# Generate a response from the custom chatbot using the OpenAI API
response = openai.Model(chatbot_model, params={"prompt": prompt}).generate()
chatbot_response = response["data"]["text"]

# Print the chatbot's response
# Once train we will pass this response to our GET API
print(chatbot_response)