import streamlit as st
import os

from config import (
    APP_TITLE, APP_SUBTITLE, DEFAULT_MODEL, 
    AVAILABLE_MODELS, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
)
from prompts import PERSONAS
from utils.groq_client import generate_chat_response
from utils.helpers import init_session_state, clear_chat, reset_conversation
from utils.styles import inject_custom_css
from utils.export_chat import export_to_txt, export_to_pdf

# Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize styles and session
inject_custom_css()
init_session_state()

# --- Sidebar ---
with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.title("Settings")
    
    # Persona Selection
    selected_persona = st.selectbox(
        "AI Persona",
        options=list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.current_persona)
    )
    
    if selected_persona != st.session_state.current_persona:
        st.session_state.current_persona = selected_persona
        clear_chat()
        st.rerun()
        
    st.info(PERSONAS[selected_persona]["description"])
    
    st.markdown("---")
    
    # Model configuration
    selected_model = st.selectbox("Model", options=AVAILABLE_MODELS, index=0)
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=DEFAULT_TEMPERATURE, step=0.1)
    max_tokens = st.slider("Max Tokens", min_value=100, max_value=8192, value=DEFAULT_MAX_TOKENS, step=100)
    
    st.markdown("---")
    
    # Chat Controls
    if st.button("New Conversation", use_container_width=True):
        reset_conversation()
        st.rerun()
        
    if st.button("Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()
        
    st.markdown("---")
    st.subheader("About")
    st.caption("AI MultiVerse Chatbot powered by Groq API. Explore different AI personalities for various tasks.")

# --- Main Area ---
st.title(APP_TITLE)
st.subheader(APP_SUBTITLE)

# Show prompt suggestions if chat is empty
if not st.session_state.messages:
    st.markdown("### Suggested Prompts")
    cols = st.columns(2)
    suggestions = PERSONAS[st.session_state.current_persona]["suggestions"]
    for i, suggestion in enumerate(suggestions):
        col_idx = i % 2
        with cols[col_idx]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                # When a suggestion is clicked, we process it as user input
                st.session_state.prompt_trigger = suggestion

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat Input
user_input = st.chat_input("Type your message here...")

# Handle triggered prompt from suggestions
if hasattr(st.session_state, 'prompt_trigger'):
    user_input = st.session_state.prompt_trigger
    del st.session_state.prompt_trigger

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Prepare messages for API (including system prompt)
    api_messages = [{"role": "system", "content": PERSONAS[st.session_state.current_persona]["system_prompt"]}]
    api_messages.extend(st.session_state.messages)
    
    # Generate response with typing indicator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_stream = generate_chat_response(
                messages=api_messages,
                model=selected_model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            full_response = st.write_stream(response_stream)
            
    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Export Options ---
if st.session_state.messages:
    st.markdown("---")
    cols = st.columns(4)
    with cols[0]:
        if st.button("Export to TXT", use_container_width=True):
            filepath = export_to_txt(st.session_state.messages, st.session_state.current_persona)
            st.success(f"Exported to {filepath}")
    with cols[1]:
        if st.button("Export to PDF", use_container_width=True):
            try:
                filepath = export_to_pdf(st.session_state.messages, st.session_state.current_persona)
                st.success(f"Exported to {filepath}")
            except Exception as e:
                st.error(f"Failed to export PDF: {str(e)}")
