import streamlit as st
import os

from config import (
    APP_TITLE, DEFAULT_MODEL, 
    AVAILABLE_MODELS, DEFAULT_TEMPERATURE
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
    # Persona Selection
    selected_persona = st.selectbox(
        "Who do you want to talk to?",
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
    
    # Replaced Max Tokens / Temp with SOME NAME to match screenshot
    some_name_val = st.slider("SOME NAME", min_value=0, max_value=10, value=10, step=1)
    
    st.markdown("---")
    
    # Chat Controls
    if st.button("New Conversation", use_container_width=True):
        reset_conversation()
        st.rerun()
        
    if st.button("Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

# --- Main Area ---
st.title(APP_TITLE)

st.markdown("Say something:")

# Use a form to capture the user input and the SEND button
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Say something:", label_visibility="collapsed")
    submitted = st.form_submit_button("SEND")

# Show prompt suggestions if chat is empty
if not st.session_state.messages:
    st.markdown("### Suggested Prompts")
    cols = st.columns(2)
    suggestions = PERSONAS[st.session_state.current_persona]["suggestions"]
    for i, suggestion in enumerate(suggestions):
        col_idx = i % 2
        with cols[col_idx]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.prompt_trigger = suggestion

# Handle triggered prompt from suggestions or form submission
trigger = None
if hasattr(st.session_state, 'prompt_trigger'):
    trigger = st.session_state.prompt_trigger
    del st.session_state.prompt_trigger
elif submitted and user_input.strip():
    trigger = user_input.strip()

if trigger:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": trigger})
        
    # Prepare messages for API (including system prompt)
    api_messages = [{"role": "system", "content": PERSONAS[st.session_state.current_persona]["system_prompt"]}]
    api_messages.extend(st.session_state.messages)
    
    # Generate response
    with st.spinner("Thinking..."):
        # We process the stream into a full string then display it
        # Since we aren't using st.chat_message for the generation stream anymore,
        # we just resolve the generator immediately
        stream = generate_chat_response(
            messages=api_messages,
            model=selected_model,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=some_name_val * 100 if some_name_val > 0 else 100
        )
        full_response = "".join(list(stream))
            
    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Display chat messages (History below input)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
