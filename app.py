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

# ---------------- APP UI ----------------

st.title("🤖 NLP Multi-Modal AI App")
st.subheader("Chatbot + Image Generator")

option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chatbot", "Image Generator"]
)

# =====================================================
# CHATBOT
# =====================================================

if option == "Chatbot":

    st.header("💬 AI Chatbot")

    user_input = st.text_input("Enter your message")

    if st.button("Send"):

        if user_input.strip() == "":
            st.warning("Please enter a message")

        else:

            with st.spinner("Thinking..."):

                payload = {
                    "inputs": user_input
                }

                try:

                    response = requests.post(
                        CHAT_API_URL,
                        headers=headers,
                        json=payload,
                        timeout=60
                    )

                    if response.status_code == 200:

                        result = response.json()

                        # FLAN-T5 output
                        if isinstance(result, list):
                            generated_text = result[0]["generated_text"]
                            st.success(generated_text)

                        else:
                            st.write(result)

                    else:

                        st.error("Chatbot request failed")

                        st.write("Status Code:", response.status_code)

                        try:
                            st.json(response.json())
                        except:
                            st.write(response.text)

                except requests.exceptions.ConnectionError:
                    st.error("Connection failed. Check internet/API.")

                except requests.exceptions.Timeout:
                    st.error("Request timed out.")

                except Exception as e:
                    st.error(f"Error: {e}")

# =====================================================
# IMAGE GENERATOR
# =====================================================

if option == "Image Generator":

    st.header("🎨 AI Image Generator")

    prompt = st.text_input("Describe your image")

    if st.button("Generate Image"):

        if prompt.strip() == "":
            st.warning("Please enter a prompt")

        else:

            with st.spinner("Generating image..."):

                payload = {
                    "inputs": prompt
                }

                try:

                    response = requests.post(
                        IMAGE_API_URL,
                        headers=headers,
                        json=payload,
                        timeout=120
                    )

                    if response.status_code == 200:

                        image = Image.open(BytesIO(response.content))

                        st.image(
                            image,
                            caption="Generated Image",
                            use_container_width=True
                        )

                    else:

                        st.error("Image generation failed")

                        st.write("Status Code:", response.status_code)

                        try:
                            st.json(response.json())
                        except:
                            st.write(response.text)

                except requests.exceptions.ConnectionError:
                    st.error("Connection failed.")

                except requests.exceptions.Timeout:
                    st.error("Request timed out.")

                except Exception as e:
                    st.error(f"Error: {e}")

        else:
            st.error("Image generation failed")
