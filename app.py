import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import utils
from PIL import Image

def initialize_session_state():
    st.session_state.setdefault('history', [])
    st.session_state.setdefault('generated', ["Hello! I am here to provide answers to questions extracted from uploaded PDF files."])
    st.session_state.setdefault('past', ["Hello Buddy!"])
    st.session_state.setdefault('pdf_files', None)
    st.session_state.setdefault('vector_store', None)

def create_conversational_chain(llm, vector_store):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        chain_type='stuff',
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
        memory=memory
    )
    return chain

def display_chat(conversation_chain):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask me questions from uploaded PDF", key='input')
            submit_button = st.form_submit_button(label='Send ⬆️')
        
        if submit_button and user_input:
            generate_response(user_input, conversation_chain)
    
    display_generated_responses(reply_container)

def generate_response(user_input, conversation_chain):
    with st.spinner('Spinning a snazzy reply...'):
        output = conversation_chat(user_input, conversation_chain, st.session_state['history'])
    
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

def conversation_chat(user_input, conversation_chain, history):
    result = conversation_chain.invoke({"question": user_input, "chat_history": history})
    history.append((user_input, result["answer"]))
    return result["answer"]

def display_generated_responses(reply_container):
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=f"{i}_user", avatar_style="adventurer")
                message(st.session_state["generated"][i], key=str(i), avatar_style="bottts")

def main():
    initialize_session_state()
    
    st.set_page_config(page_title="PDF Analyzer Bot", page_icon="🤖", layout="wide")
    st.title("📄 PDF Analyzer Bot 🤖")
    
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

    st.sidebar.title("Upload PDF and Analyze")
    pdf_files = st.sidebar.file_uploader("Choose PDF files", accept_multiple_files=True, type=["pdf"])
    
    if pdf_files:
        st.session_state.pdf_files = pdf_files
    else:
        st.sidebar.warning("Please upload at least one PDF file.")

    button = st.sidebar.button("Analyze")

    index_path = "faiss_index"

    if button and st.session_state.pdf_files:
        with st.spinner('Analyzing PDF files...'):
            llm = utils.create_llm()
            vector_store = utils.create_vector_store(st.session_state.pdf_files, index_path)
            st.session_state.vector_store = vector_store

            if vector_store:
                chain = create_conversational_chain(llm, vector_store)
                display_chat(chain)
            else:
                st.sidebar.success("App is ready for analysis.")
    else:
        with st.spinner('Loading vector store...'):
            vector_store = utils.load_vector_store(index_path)
            if vector_store:
                st.session_state.vector_store = vector_store
                llm = utils.create_llm()
                chain = create_conversational_chain(llm, vector_store)
                display_chat(chain)
            else:
                st.sidebar.info("Please upload PDF files and click Analyze to get started.")

if __name__ == "__main__":
    main()
