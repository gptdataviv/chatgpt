from langchain.chat_models import ChatOpenAI
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain, ConversationChain
import json

llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-0301')
original_chain = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

original_chain.run('Start noting down thing i say.')

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
reloaded_chain.run('Vini plays for Real Madrid')

reloaded_chain.run('Vini wears jersey number 7')

reloaded_chain.run('what did you note down on Vini')

print(reloaded_chain.memory.chat_memory.messages)