import streamlit as st

st.set_page_config(
    page_title="The Identity Echo Interface",
    page_icon="O",
    layout="centered"
)
st.title("The Identity Echo Interface")
st.write(
    "Welcome! Please enter your name and message below, then click **Transmit** to send your message."
)
st.divider()
user_name = st.text_input("Enter your Name")
user_message = st.text_input("Enter your Message")
st.divider()
if st.button("🚀 Transmit"):
    if user_name.strip() == "":
        st.error("Please provide your name.")
    elif user_message.strip() == "":
        st.warning("Please type a message to transmit.")
    else:
        st.success(
            f"Transmission successful! Greetings, {user_name}. "
            f"We received your message: {user_message}"
        )
        
