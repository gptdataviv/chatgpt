from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, ConversationChain
import json
from gptapis.models import ChatData

class Chats():
    def create_chat(user_id: int, prompt_text: str):
        llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-0301')
        original_chain = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationBufferMemory()
        )
        original_chain.run(prompt_text)
        extracted_messages = original_chain.memory.chat_memory.messages
        ingest_to_db = messages_to_dict(extracted_messages)
        
        # Create an instance of ChatData
        new_chat = ChatData(
            user_id=user_id,
            chat_data=ingest_to_db
        )
        
        # Save to the database
        new_chat.save()
        
        return original_chain
    
    def get_all_chats():
        return []
    
    def get_chat_history():
        return []
    
    def save_chat_history():
        return []
    
    def save_messages_to_db(user_id: int, chat_id: int, messages: str):
        return True