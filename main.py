import os
from langchain import hub
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from ingest import docs,embeddings,qdrant
from langchain.chains import (
    ConversationalRetrievalChain,
)
from langchain.memory import ChatMessageHistory, ConversationBufferMemory

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "db")

rag_prompt_mistral = hub.pull("rlm/rag-prompt-mistral")

def load_model():
    llm = Ollama(
        model="mistral",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm


def retrieval_qa_chain(llm, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": rag_prompt_mistral},
        return_source_documents=True,
    )
    return qa_chain


def create_qa_bot():
    llm = load_model()
    DB_PATH = DB_DIR
   
    vectorstore = Qdrant.from_documents(
    docs,
    embeddings, 
    path = DB_PATH,
    collection_name="my_documents",
    )
    
    qa = retrieval_qa_chain(llm, vectorstore)
    return qa

qa_bot = create_qa_bot()



message_history = ChatMessageHistory()
memory = ConversationBufferMemory(
    memory_key="chat_history",
    output_key="answer",
    chat_memory=message_history,
    return_messages=True,
    )

chain = ConversationalRetrievalChain.from_llm(
    Ollama(model="mistral"),  # Using Ollama directly
    chain_type="stuff",
    retriever=qdrant.as_retriever(),
    memory=memory,
    return_source_documents=True,
    )
def answer_question(question):
    result = chain.invoke(question)
    return result['answer'], result['source_documents']
