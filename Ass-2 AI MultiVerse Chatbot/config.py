import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Details
APP_TITLE = "The MULTIVERSE OF CHATBOTS"
APP_SUBTITLE = "Explore Multiple AI Personalities in One Interface"

# Groq Configuration
DEFAULT_MODEL = "llama-3.1-8b-instant"
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024

# Theme settings
THEME_COLORS = {
    "primary": "#1E3A8A", # Deep blue
    "secondary": "#3B82F6", # Bright blue
    "background": "#F8FAFC", # Light slate
    "surface": "#FFFFFF", # White
    "text": "#1E293B", # Slate gray
    "text_light": "#64748B" # Light slate gray
}

# Directories
EXPORTS_DIR = "chat_exports"
os.makedirs(EXPORTS_DIR, exist_ok=True)
