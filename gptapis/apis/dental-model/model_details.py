from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, ConversationChain
import json,time,os

llm = ChatOpenAI(api_key=os.environ["OPENAI_API_KEY"],temperature=0,model_name='gpt-3.5-turbo-0301')
original_chain = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

original_chain.run('Can you note down the symptoms i speak?')

extracted_messages = original_chain.memory.chat_memory.messages
ingest_to_db = messages_to_dict(extracted_messages)
retrieve_from_db = json.loads(json.dumps(ingest_to_db))

retrieved_messages = messages_from_dict(retrieve_from_db)
retrieved_chat_history = ChatMessageHistory(messages=retrieved_messages)
retrieved_memory = ConversationBufferMemory(chat_memory=retrieved_chat_history)

reloaded_chain = ConversationChain(
    llm=llm,
    verbose=True,
    memory=retrieved_memory
)
reloaded_chain.run('The patient face is swollen')

reloaded_chain.run('The patient feels pain is right molars')

time.sleep(60)
reloaded_chain.run('List down the symptoms which i asked you to note down and suggest remedies for them.')

print(reloaded_chain.memory.chat_memory.messages)