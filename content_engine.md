<div align="center">
    <h1>Content Engine 🤖</h1>
</div>

Welcome to the **Content Engine** project! This system is designed to analyze and compare multiple PDF documents using Retrieval Augmented Generation (RAG) techniques. It enables users to retrieve, assess, and generate insights from documents, all within an interactive chatbot interface built with Streamlit.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)

## Overview

In this assignment, you'll be working on creating a Content Engine that leverages advanced AI/ML techniques to analyze PDF documents. The system utilizes a combination of document processing, embedding models, a vector store for efficient querying, and a local instance of a large language model (LLM) for generating insights. The chatbot interface built with Streamlit allows users to interactively query and compare information across uploaded documents.

## Architecture

The Content Engine's architecture is designed to be modular, scalable, and privacy-focused:

- **User Interface (Streamlit)**:
  - Provides a user-friendly interface for uploading PDFs, asking questions, and viewing comparative insights.

- **Backend Processing**:
  - **Document Processing**: Extracts text content from uploaded PDF documents.
  - **Embedding Generation**: Converts document text into numerical representations using an embedding model (MiniLM).
  - **Vector Store (FAISS)**: Manages and queries document embeddings efficiently for retrieval tasks.
  - **Retrieval Engine**: Performs similarity search using FAISS to retrieve relevant documents based on user queries.
  - **Language Model (LLM)**: Provides contextual insights and answers based on retrieved documents and user queries.

- **Data Flow**:
  - Users upload PDFs through the Streamlit interface.
  - Text is extracted from PDFs and converted into embeddings.
  - Embeddings are stored in FAISS for fast retrieval.
  - Users interact with the chatbot interface to ask questions and receive insights.

## Setup

To run the Content Engine locally, follow these steps:

### Prerequisites

- Python 3.8 or higher
- Pip (Python package installer)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd Content_Engine
