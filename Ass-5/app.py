import os
import json
import tempfile
from io import BytesIO

import requests
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from gtts import gTTS
from groq import Groq

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Multi-Modal Visual Novel",
    page_icon="📖",
    layout="wide"
)

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

# -----------------------------
# CACHE GROQ CLIENT
# -----------------------------
@st.cache_resource
def load_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY not found in .env file.")
        st.stop()

    return Groq(api_key=api_key)

client = load_client()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🎮 Story Settings")

genre = st.sidebar.selectbox(
    "Story Genre",
    [
        "Fantasy",
        "Sci-Fi",
        "Mystery",
        "Horror",
        "Adventure"
    ]
)

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Anime",
        "Realistic",
        "Pixel Art",
        "Watercolor",
        "Digital Painting"
    ]
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "scenes" not in st.session_state:
    st.session_state.scenes = []

if "started" not in st.session_state:
    st.session_state.started = False

# -----------------------------
# TITLE
# -----------------------------
st.title("📖 AI Multi-Modal Visual Novel")
st.caption("Powered by Groq + Pollinations + gTTS")

# -----------------------------
# SYSTEM PROMPT
# -----------------------------
SYSTEM_PROMPT = f"""
You are an AI Visual Novel Engine.

Story Genre:
{genre}

Art Style:
{art_style}

Always return ONLY valid JSON.

Format:

{{
"story_text":"Narrate the story.",
"image_prompt":"Highly detailed image prompt based on current scene.",
"options":[
"Choice 1",
"Choice 2",
"Choice 3"
]
}}

Rules:

1. Return ONLY JSON.
2. Do not wrap inside markdown.
3. image_prompt should be cinematic.
4. options must contain exactly 3 choices.
5. Continue the story based on the user's choice.
"""

# -----------------------------
# GROQ FUNCTION
# -----------------------------
def ask_ai(user_input):

    try:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(st.session_state.history)

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.9,
            max_tokens=900
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)

        st.session_state.history.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.history.append(
            {
                "role": "assistant",
                "content": text
            }
        )

        return data

    except Exception as e:
        st.error(f"Groq Error: {e}")
        return None

# -----------------------------
# IMAGE GENERATION
# -----------------------------
def generate_image(prompt):

    try:

        url = (
            "https://image.pollinations.ai/prompt/"
            + requests.utils.quote(prompt)
        )

        response = requests.get(url, timeout=30)

        response.raise_for_status()

        return Image.open(BytesIO(response.content))

    except Exception:

        st.toast("Image server is busy, skipping visual...")

        return None


# -----------------------------
# TEXT TO SPEECH
# -----------------------------
def play_audio(text):

    try:

        tts = gTTS(
            text=text,
            lang="en",
            slow=False
        )

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp.name)

        st.audio(temp.name)

    except Exception:

        st.toast("Unable to generate narration.")


# -----------------------------
# DISPLAY STORY SCENES
# -----------------------------
for index, scene in enumerate(st.session_state.scenes):

    st.markdown("---")

    st.subheader(f"Scene {index + 1}")

    image = generate_image(scene["image_prompt"])

    if image is not None:
        st.image(image, use_container_width=True)

    st.write(scene["story_text"])

    play_audio(scene["story_text"])


# -----------------------------
# START BUTTON
# -----------------------------
if not st.session_state.started:

    st.info(
        "Click the button below to begin your adventure."
    )

    if st.button(
        "🚀 Start Adventure",
        use_container_width=True
    ):

        data = ask_ai("Start the story.")

        if data is not None:

            st.session_state.started = True

            st.session_state.scenes.append(data)

            st.rerun()


# -----------------------------
# CURRENT SCENE
# -----------------------------
if st.session_state.started:

    current_scene = st.session_state.scenes[-1]

    st.markdown("---")

    st.subheader("Current Scene")

    image = generate_image(
        current_scene["image_prompt"]
    )

    if image is not None:
        st.image(
            image,
            use_container_width=True
        )

    st.write(current_scene["story_text"])

    play_audio(current_scene["story_text"])

    st.markdown("### Choose Your Next Action")

    # -----------------------------
    # DYNAMIC CHOICE BUTTONS
    # -----------------------------
    options = current_scene.get("options", [])

    if len(options) == 0:
        st.warning("No options returned by the AI.")
    else:

        for option in options:

            if st.button(
                option,
                use_container_width=True,
                key=f"choice_{option}"
            ):

                with st.spinner("Generating next scene..."):

                    next_scene = ask_ai(option)

                if next_scene is not None:

                    st.session_state.scenes.append(next_scene)

                    st.rerun()


# -----------------------------
# SIDEBAR INFO
# -----------------------------
st.sidebar.markdown("---")

st.sidebar.success(
    f"Scenes Generated : {len(st.session_state.scenes)}"
)

st.sidebar.info(
    f"Conversation Messages : {len(st.session_state.history)}"
)

# -----------------------------
# RESTART STORY
# -----------------------------
if st.sidebar.button("🔄 Restart Story"):

    st.session_state.history = []
    st.session_state.scenes = []
    st.session_state.started = False

    st.rerun()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.caption(
    "Built using Streamlit • Groq • Pollinations AI • gTTS"
)