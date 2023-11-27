from django.http import JsonResponse
from .get_client import ClientDetails

class prompt():
    def gptprompt(question_text):
        # Function to initialize and utilize OpenAI Client
        client = ClientDetails.initialize_client()
        # Send the prompt to the GPT API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{
                "content": question_text,
                "role": "user"
            }],
            temperature=0.9,
            max_tokens=1000
        )
        return response.choices[0].message.content