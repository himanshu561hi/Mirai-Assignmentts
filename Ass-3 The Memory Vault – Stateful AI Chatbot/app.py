import os
import streamlit as st
from groq import Groq, GroqError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Streamlit Page Configuration
st.set_page_config(
    page_title="The Memory Vault",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Configuration for Groq API
API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

# CSS for UI improvements
st.markdown("""
<style>
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 12px;
        color: #888;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# Personality options mapping to System Prompts
PERSONALITIES = {
    "Helpful Assistant": "You are a helpful, respectful, and honest assistant. Always answer as helpfully as possible, while being safe.",
    "Friendly": "You are a friendly and enthusiastic companion. Use a warm, positive tone and be conversational.",
    "Professional": "You are a highly professional and articulate assistant. Keep your responses concise, formal, and objective.",
    "Teacher": "You are a patient and knowledgeable teacher. Break down complex topics so they are easy to understand, providing examples when necessary.",
    "Funny": "You are a hilarious and witty assistant. Use appropriate humor and keep things lighthearted while answering."
}

# -----------------
# Sidebar Component
# -----------------
with st.sidebar:
    st.header("Settings")
    
    # Select Personality
    selected_personality = st.selectbox(
        "Choose Personality:",
        list(PERSONALITIES.keys())
    )
    
    # Temperature Slider
    temperature = st.slider(
        "Temperature:",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values make it more focused."
    )
    
    # Clear Chat Button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.subheader("About")
    st.markdown("This stateful AI Chatbot is built with Streamlit and Groq. It remembers the context of your conversation across reruns.")

# -----------------
# Main Chat Area
# -----------------
st.title("The Memory Vault")
st.subheader("Stateful AI Chatbot")

# Verify API Key and Connection
if not API_KEY:
    st.error("GROQ_API_KEY is missing. Please set it in your .env file.")
    st.stop()

try:
    # Initialize Groq Client
    client = Groq(api_key=API_KEY)
    st.sidebar.success("API Connection: Online")
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

# Initialize Session State for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input & Processing
if prompt := st.chat_input("Say something..."):
    # Immediately save and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Prepare conversation history for the API
    system_prompt = PERSONALITIES[selected_personality]
    conversation_history = [{"role": "system", "content": system_prompt}] + st.session_state.messages
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=conversation_history,
                    temperature=temperature
                )
                
                reply = response.choices[0].message.content
                
                if reply:
                    st.markdown(reply)
                    # Save assistant response to session state
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error("Received an empty response from the API.")
                    
            except APIConnectionError:
                st.error("Network error: Could not connect to Groq API. Please check your internet connection.")
            except RateLimitError:
                st.error("Rate limit exceeded. Please wait a moment and try again.")
            except GroqError as e:
                st.error(f"Groq API Error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

# Footer
st.markdown('<div class="footer">Built with Streamlit & Groq API</div>', unsafe_allow_html=True)
