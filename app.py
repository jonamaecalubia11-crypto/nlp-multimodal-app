import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Hugging Face API Token
API_TOKEN = "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"

# Models
CHAT_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Streamlit page
st.set_page_config(page_title="NLP Multi-Modal AI App")

st.title("🤖 NLP Multi-Modal AI App")
st.subheader("Chat + AI Image Generator")

# Sidebar
option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chatbot", "Image Generator"]
)

# ---------------- CHATBOT ----------------
if option == "Chatbot":

    st.header("💬 AI Chatbot")

    user_input = st.text_input("Enter your message")

    if st.button("Send"):

        payload = {
            "inputs": user_input
        }

        response = requests.post(
            CHAT_API_URL,
            headers=headers,
            json=payload
        )

        result = response.json()

        try:
            st.success(result["generated_text"])
        except:
            st.error("Error generating response")

# ---------------- IMAGE GENERATOR ----------------
if option == "Image Generator":

    st.header("🎨 AI Image Generator")

    prompt = st.text_input("Describe your image")

    if st.button("Generate Image"):

        payload = {
            "inputs": prompt
        }

        response = requests.post(
            IMAGE_API_URL,
            headers=headers,
            json=payload
        )

        if response.status_code == 200:

            image = Image.open(BytesIO(response.content))

            st.image(image, caption="Generated Image")

        else:
            st.error("Image generation failed")