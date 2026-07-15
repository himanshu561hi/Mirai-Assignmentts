import streamlit as st
import urllib.parse
import urllib.request
import urllib.error
import random

# Page configuration for better UI
st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="centered"
)

# Constants for features
MAGIC_ENHANCE_PROMPT = "masterpiece, 8k resolution, highly detailed, cinematic lighting, trending on artstation, unreal engine 5 render, award winning, ultra realistic"

SURPRISE_PROMPTS = [
    "Astronaut riding a horse on Mars",
    "Giant whale flying over New York",
    "Cyberpunk chai shop in India",
    "Floating islands above the Himalayas",
    "Samurai panda drinking coffee",
    "Ancient temple inside a volcano",
    "AI robot painting Mona Lisa",
    "Dragon sleeping in a modern city",
    "Underwater library with glowing books",
    "Castle floating in the clouds"
]

def build_prompt(user_prompt: str, art_style: str, magic_enhance: bool) -> str:
    """Builds the final prompt to be sent to the API."""
    final_prompt = user_prompt.strip()
    
    if art_style and art_style != "None":
        final_prompt += f" in {art_style} style"
        
    if magic_enhance:
        final_prompt += f", {MAGIC_ENHANCE_PROMPT}"
        
    return final_prompt

def build_url(prompt: str, width: int, height: int) -> str:
    """Constructs the API URL with URL encoding and query parameters."""
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}"
    return url

def generate_image(url: str):
    """Fetches the image from the API and handles errors."""
    try:
        # Handle macOS SSL certificate issues by creating an unverified context
        import ssl
        ssl_context = ssl._create_unverified_context()
        
        # Provide a reasonable timeout for the API request
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=30, context=ssl_context)
        return response.read()
    except urllib.error.URLError as e:
        if isinstance(e.reason, TimeoutError):
            st.error("⏳ Request timed out. The server took too long to respond.")
        else:
            st.error(f"🌐 Network error or connection issue: {e.reason}")
    except urllib.error.HTTPError as e:
        st.error(f"🔌 API Error: HTTP {e.code} - {e.reason}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
    return None

def main():
    st.title("🎨 AI Image Studio")
    st.subheader("Generate stunning AI artwork in seconds.")
    
    # Sidebar Organization
    st.sidebar.header("⚙️ Settings")
    
    # User inputs in sidebar
    art_style = st.sidebar.selectbox(
        "Art Style", 
        ["None", "Anime", "Photorealistic", "3D Render", "Watercolor", "Oil Painting", "Cyberpunk", "Sketch"]
    )
    
    # Fixed the swt.sidebar.slider typo and implemented width/height
    width = st.sidebar.slider("Width", min_value=256, max_value=1920, value=768, step=16)
    height = st.sidebar.slider("Height", min_value=256, max_value=1920, value=768, step=16)
    
    magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance", value=False)
    
    # Main form
    prompt = st.text_input("Enter your prompt:", placeholder="e.g., A futuristic city at sunset...")
    
    col1, col2 = st.columns(2)
    with col1:
        generate_btn = st.button("Generate Image", type="primary", use_container_width=True)
    with col2:
        surprise_btn = st.button("🎲 Surprise Me!", use_container_width=True)
    
    # Determine if we need to generate an image
    trigger_generation = False
    
    if surprise_btn:
        prompt = random.choice(SURPRISE_PROMPTS)
        st.success(f"🎲 Surprise Prompt Selected: **{prompt}**")
        trigger_generation = True
    elif generate_btn:
        if not prompt.strip():
            st.warning("⚠️ Please enter a prompt or click 'Surprise Me!'.")
        else:
            trigger_generation = True
            
    # Execute generation if triggered
    if trigger_generation and prompt.strip():
        final_prompt = build_prompt(prompt, art_style, magic_enhance)
        url = build_url(final_prompt, width, height)
        
        # Show spinner while generating
        with st.spinner("Generating masterpiece..."):
            image_bytes = generate_image(url)
            
        if image_bytes:
            st.success("✅ Image Generated Successfully")
            
            # Display selected settings
            st.info(f"""
**Art Style:** {art_style}  
**Resolution:** {width} × {height}  
**Magic Enhance:** {'Enabled' if magic_enhance else 'Disabled'}
            """)
            
            # Show the generated image
            st.image(image_bytes, caption=prompt, use_container_width=True)
            
            # Improve download button with dynamic filename
            file_name = f"{art_style.lower().replace(' ', '_')}_image.png" if art_style != "None" else "ai_image.png"
            
            st.download_button(
                label="⬇️ Download Image",
                data=image_bytes,
                file_name=file_name,
                mime="image/png"
            )

if __name__ == "__main__":
    main()
