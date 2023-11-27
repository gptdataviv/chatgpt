from openai import OpenAI
from .creds import Creds

class ClientDetails():
    def initialize_client():
        GPT_API_KEY = Creds.get_key('GPT')
        client = OpenAI(
            api_key=GPT_API_KEY,
        )
        return client