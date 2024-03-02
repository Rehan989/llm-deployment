import os
import warnings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
)
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import Qdrant

warnings.simplefilter("ignore")

ABS_PATH: str = os.path.dirname(os.path.abspath(__file__))
DB_DIR: str = os.path.join(ABS_PATH, "db")


# Create vector database
# def create_vector_database():
#     """
#     Creates a vector database using document loaders and embeddings.

#     This function loads data from PDF, markdown and text files in the 'data/' directory,
#     splits the loaded documents into chunks, transforms them into embeddings using OllamaEmbeddings,
#     and finally persists the embeddings into a Chroma vector database.

#     """
    # Initialize loaders for different file types
pdf_loader = DirectoryLoader("data/", glob="**/*.pdf", loader_cls=PyPDFLoader)
loaded_documents = pdf_loader.load()
    #len(loaded_documents)

    # Split loaded documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=40)
docs = text_splitter.split_documents(loaded_documents)
    #len(chunked_documents)
    #chunked_documents[0]

    # Initialize Ollama Embeddings
embeddings = OllamaEmbeddings(model="mistral")
url = "localhost:6333"
    # Create and persist a qdrant vector database from the chunked documents
qdrant = Qdrant.from_documents(
    docs,
    embeddings,
   # path=DB_DIR,
    url=url,
    collection_name="my_documents"
)
print(f"DB directory after creation: {DB_DIR}")
if os.path.exists(DB_DIR):
    print(f"Contents of DB directory: {os.listdir(DB_DIR)}")
# if __name__ == "__main__":
#     create_vector_database()
