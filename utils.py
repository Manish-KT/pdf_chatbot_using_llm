from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

import os
import tempfile
from typing import List
from tqdm import tqdm

def create_llm():
    """
    Create an instance of Mistral 7B GGUF format LLM using LlamaCpp

    returns:
    - llm: An instance of Mistral 7B LLM
    """
    llm = LlamaCpp(
        streaming=True,
        model_path="artifacts/mistral-7b-instruct-v0.2.Q2_K.gguf",
        temperature=0.3,
        top_p=0.8,
        verbose=True,
        n_ctx=4096  # Context Length
    )
    return llm


def create_embedding_model():
    """
    Create an instance of HuggingFace Embeddings

    returns:
    - embeddings: An instance of HuggingFace Embeddings
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                 model_kwargs={'device': 'cpu'})

def create_vector_store(pdf_files: List, index_path: str):
    """
    Create In-memory FAISS vector store using uploaded PDFs and save it to a file

    Args:
    - pdf_files(List): PDF files uploaded
    - index_path(str): Path to save the FAISS index

    returns:
    - vector_store: In-memory Vector store for further processing in chat app
    """
    vector_store = None

    if pdf_files:
        text = []
        
        for file in tqdm(pdf_files, desc="Processing files"):
            # Get the file and check its extension
            file_extension = os.path.splitext(file.name)[1]
            # Write the PDF file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name
            # Load the PDF files using PyPdf library 
            loader = None
            if file_extension == ".pdf":
                loader = PyPDFLoader(temp_file_path)

            # Load if text file
            if loader:
                text.extend(loader.load())
                os.remove(temp_file_path)

        # Split the file into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=10)
        text_chunks = text_splitter.split_documents(text)

        # Create embeddings
        embeddings = create_embedding_model()

        # Create vector store and store document chunks using embedding model
        vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
        # Save the FAISS index to a file
        vector_store.save_local(index_path)

    return vector_store

def load_vector_store(index_path: str):
    """
    Load FAISS vector store from a local file

    Args:
    - index_path(str): Path to load the FAISS index from

    returns:
    - vector_store: Loaded FAISS Vector store
    """
    if os.path.exists(index_path):
        return FAISS.load_local(
            index_path, 
            embeddings=create_embedding_model(), 
            allow_dangerous_deserialization=True
        )
    return None
