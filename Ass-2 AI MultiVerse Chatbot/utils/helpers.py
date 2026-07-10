import streamlit as st
from prompts import PERSONAS

def init_session_state():
    """Initializes default Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "current_persona" not in st.session_state:
        st.session_state.current_persona = list(PERSONAS.keys())[0]

def clear_chat():
    """Clears the chat history."""
    st.session_state.messages = []
    
def reset_conversation():
    """Resets the chat and keeps the persona."""
    clear_chat()
    # Add initial system message based on persona if needed,
    # though it's typically injected at API call time rather than UI time.
