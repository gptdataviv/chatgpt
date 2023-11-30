from openai import OpenAI
import os

class ClientDetails():
    def initialize_client():
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )
        return client