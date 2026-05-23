import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout
from PIL import Image
from io import BytesIO
import os

# ======================================
# PAGE SETTINGS
# ======================================
st.set_page_config(page_title="NLP Multi-Modal AI App")

st.title("🤖 NLP Multi-Modal AI App")
st.subheader("Chatbot + AI Image Generator")

# ======================================
# DIAGNOSTIC STORAGE & SSL FIX
# ======================================
# Fix 1: Disables SSL bundle environment bugs common in cloud container endpoints
os.environ['CURL_CA_BUNDLE'] = '' 

# Fix 2: Handle both dictionary and direct formats for st.secrets safely
try:
    if isinstance(st.secrets.get("HF_TOKEN"), dict):
        API_TOKEN = st.secrets["HF_TOKEN"]["token"]
    else:
        API_TOKEN = st.secrets.get("HF_TOKEN")
except Exception as e:
    st.error(f"Secrets Configuration Error: {e}")
    API_TOKEN = None

# If API_TOKEN didn't load from HF_TOKEN, use a fallback direct assignment to test
if not API_TOKEN:
    API_TOKEN = "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"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

CHAT_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

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

            with st.spinner("Thinking..."):

                payload = {
                    "inputs": user_input,
                    "parameters": {"max_new_tokens": 100}  # Helps FLAN-T5 generate better responses
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

                        # Properly parsing Hugging Face's return list format
                        if isinstance(result, list) and len(result) > 0:
                            generated_text = result[0].get("generated_text", "")
                            st.success(generated_text)
                        elif isinstance(result, dict) and "generated_text" in result:
                            st.success(result["generated_text"])
                        else:
                            st.write(result)

                    else:

                        st.error("Chatbot request failed")
                        st.write("Status Code:", response.status_code)

                        try:
                            st.json(response.json())
                        except:
                            st.write(response.text)

              except ConnectionError as ce:
                st.error(f"Connection failed: {ce}")
                except Timeout:
                    st.error("Request timed out.")

                except Exception as e:
                    st.error(f"Error: {e}")

# ======================================
# IMAGE GENERATOR
# ======================================

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

                except ConnectionError:
                    st.error("Connection failed.")

                except Timeout:
                    st.error("Request timed out.")

                except Exception as e:
                    st.error(f"Error: {e}")
