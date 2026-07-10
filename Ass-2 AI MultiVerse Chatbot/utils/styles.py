import streamlit as st
from config import THEME_COLORS

def inject_custom_css():
    """Injects custom CSS for the application theme."""
    custom_css = f"""
    <style>
        /* General Theme */
        .stApp {{
            background-color: {THEME_COLORS['background']};
            color: {THEME_COLORS['text']};
            font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {THEME_COLORS['surface']};
            border-right: 1px solid rgba(0,0,0,0.05);
            box-shadow: 2px 0 8px rgba(0,0,0,0.02);
        }}
        
        /* Chat Input */
        .stChatInputContainer {{
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.05);
            background-color: {THEME_COLORS['surface']};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            background: linear-gradient(90deg, {THEME_COLORS['primary']}, {THEME_COLORS['secondary']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }}
        
        /* Chat Messages */
        .stChatMessage {{
            background-color: {THEME_COLORS['surface']};
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
            border: 1px solid rgba(0,0,0,0.04);
        }}
        
        /* User Message specific */
        [data-testid="stChatMessage"][data-baseweb="user"] {{
            background-color: #EEF2FF;
            border: 1px solid #E0E7FF;
        }}
        
        /* Avatars */
        .stChatMessageAvatar {{
            border-radius: 8px;
        }}
        
        /* Buttons */
        .stButton>button {{
            border-radius: 8px;
            border: 1px solid {THEME_COLORS['secondary']};
            background-color: {THEME_COLORS['surface']};
            color: {THEME_COLORS['secondary']};
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        
        .stButton>button:hover {{
            background-color: {THEME_COLORS['secondary']};
            color: white;
            border-color: {THEME_COLORS['secondary']};
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
        }}
        
        /* Error messages */
        .stAlert {{
            border-radius: 12px;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
