from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# load the pdf files
loader = DirectoryLoader(path='/Users/prabhakaran/Desktop/Tushar_Projects/chatgpt/gptapis/apis/dental-model/training_data', glob="*.pdf", loader_cls=PyPDFLoader)

# split the documents into chunks
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                          chunk_overlap=50)
texts = splitter.split_documents(documents)

from langchain.embeddings import HuggingFaceEmbeddings

# load the embeddings model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'})

from langchain.vectorstores import FAISS

# create the vector store database
db = FAISS.from_documents(texts, embeddings)


# save the vector store
db.save_local("faiss")


from langchain.llms import CTransformers

def load_llm():
    """load the llm"""

    llm = CTransformers(model='/Users/prabhakaran/Desktop/Tushar_Projects/chatgpt/gptapis/apis/dental-model/training_data/llama-2-7b-chat.ggmlv3.q2_K.bin', # model available here: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
                    model_type='llama',
                    config={'max_new_tokens': 256, 'temperature': 0})
    return llm

def load_vector_store():
    # load the vector store
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'})
    db = FAISS.load_local("faiss", embeddings)
    return db

from langchain import PromptTemplate

def create_prompt_template():
    # prepare the template that provides instructions to the chatbot

    template = """Use the provided context to answer the user's question.
    If you don't know the answer, respond with "I do not know".
    Context: {context}
    Question: {question}
    Answer:
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=['context', 'question'])
    return prompt

from langchain.chains import RetrievalQA

def create_qa_chain():
    """create the qa chain"""

    # load the llm, vector store, and the prompt
    llm = load_llm()
    db = load_vector_store()
    prompt = create_prompt_template()


    # create the qa_chain
    retriever = db.as_retriever(search_kwargs={'k': 2})
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type='stuff',
                                        retriever=retriever,
                                        return_source_documents=True,
                                        chain_type_kwargs={'prompt': prompt})
    
    return qa_chain

def generate_response(query, qa_chain):

    # use the qa_chain to answer the given query
    return qa_chain({'query':query})['result']

import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title='Llama2-Chatbot')
st.header('Custom Llama2-Powered Chatbot :robot_face:')

def get_user_input():

    # get the user query
    input_text = st.text_input('Ask me anything about the use of computer vision in sports!', "", key='input')
    return input_text

# create the qa_chain
qa_chain = create_qa_chain()

# create empty lists for user queries and responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# get the user query
user_input = get_user_input()

if user_input:

    # generate response to the user input
    response = generate_response(query=user_input, qa_chain=qa_chain)

    # add the input and response to session state
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

# display conversaion history (if there is one)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) -1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')