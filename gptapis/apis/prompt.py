from openai import OpenAI
from django.http import JsonResponse

class prompt():
    GPT_API_KEY = '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'
    def gptprompt(question_text):
        client = OpenAI(
            api_key=prompt.GPT_API_KEY,
        )
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