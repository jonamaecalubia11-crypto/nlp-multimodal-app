import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ======================================
# PAGE SETTINGS
# ======================================

st.set_page_config(page_title="NLP Multi-Modal AI App")

st.title("🤖 NLP Multi-Modal AI App")

# ======================================
# API SETTINGS
# ======================================

API_TOKEN = st.secrets["API_TOKEN"]

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# ======================================
# SIDEBAR
# ======================================

option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chatbot", "Image Generator"]
)

# ======================================
# CHATBOT
# ======================================

if option == "Chatbot":

    st.header("💬 AI Chatbot")

    user_input = st.text_input("Enter your message")

    if st.button("Send"):

        if user_input.strip() == "":
            st.warning("Please enter a message")

        else:

            message = user_input.lower()

            # Simple NLP chatbot responses
            if "hello" in message or "hi" in message:
                response = "Hello! How can I help you today?"

            elif "how are you" in message:
                response = "I'm doing great! Thanks for asking."

            elif "what is ai" in message:
                response = "AI stands for Artificial Intelligence."

            elif "your name" in message:
                response = "I am your NLP Multi-Modal AI Assistant."

            elif "bye" in message:
                response = "Goodbye! Have a nice day."

            elif "python" in message:
                response = "Python is a popular programming language for AI and NLP."

            elif "streamlit" in message:
                response = "Streamlit is a Python framework for building web apps."

            else:
                response = "Sorry, I don't understand that yet."

            st.success(response)

# ======================================
# IMAGE GENERATOR
# ======================================

elif option == "Image Generator":

    st.header("🎨 AI Image Generator")

    prompt = st.text_input("Describe your image")

    if st.button("Generate Image"):

        if prompt.strip() == "":
            st.warning("Please enter a prompt")

        else:

            with st.spinner("Generating image..."):

                image_url = f"https://image.pollinations.ai/prompt/{prompt}"

                st.image(
                    image_url,
                    caption="Generated Image",
                    use_container_width=True
                )

                st.markdown(
                    f"[Download Image]({image_url})"
                )
