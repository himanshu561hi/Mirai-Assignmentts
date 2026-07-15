import streamlit as st

def inject_custom_css():
    """Injects custom CSS for the application theme."""
    custom_css = f"""
    <style>
        /* General Theme */
        .stApp {{
            font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        
        /* Headers */
        h1 {{
            text-align: center;
            font-weight: 800 !important;
            font-size: 3rem !important;
            letter-spacing: -0.02em;
            margin-bottom: 2rem !important;
        }}
        
        /* Sub-labels */
        .stMarkdown p {{
            font-weight: 500;
        }}
        
        /* Chat Messages */
        .stChatMessage {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* Input Box */
        .stTextInput input {{
            border-radius: 8px;
            background-color: #1F1F2E;
            border: 1px solid #333344;
            color: #FFFFFF;
            padding: 10px 15px;
        }}
        
        /* Buttons */
        .stButton>button {{
            border-radius: 6px;
            border: 1px solid #333344;
            background-color: transparent;
            color: #FFFFFF;
            font-weight: 500;
            padding: 0.5rem 1.5rem;
            transition: all 0.2s ease;
        }}
        
        .stButton>button:hover {{
            background-color: rgba(255, 255, 255, 0.1);
            border-color: #555566;
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
