import streamlit as st
import requests
from groq import Groq
from PIL import Image
from io import BytesIO

# ======================================
# PAGE SETTINGS
# ======================================
st.set_page_config(page_title="NLP Multi-Modal AI App", layout="centered")

st.title("🤖 NLP Multi-Modal AI App")
st.subheader("Chatbot + AI Image Generator")

# ======================================
# INITIALIZE APIS
# ======================================

# Safely load Groq Key from secrets dashboard or use a temporary local variable
if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"]
else:
    # Fallback to empty string if not configured yet so the page layout loads smoothly
    groq_key = ""

# ======================================
# SIDEBAR
# ======================================
option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chatbot", "Image Generator"]
)

# ======================================
# CHATBOT (Powered by Groq & Llama 3)
# ======================================
if option == "Chatbot":

    st.header("💬 AI Chatbot")
    
    if not groq_key:
        st.warning("⚠️ Please add your `GROQ_API_KEY` to your Streamlit Secrets panel to use the chatbot.")
    
    user_input = st.text_input("Enter your message")

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please enter a message")
        elif not groq_key:
            st.error("Missing API Key.")
        else:
            with st.spinner("Thinking..."):
                try:
                    # Initialize the Groq client
                    client = Groq(api_key=groq_key)
                    
                    # Request generation from llama3-8b model
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    
                    # Display response response block
                    response_text = completion.choices[0].message.content
                    st.success(response_text)

                except Exception as e:
                    st.error(f"Chatbot failed: {e}")

# ======================================
# IMAGE GENERATOR (Powered by Pollinations.ai)
# ======================================
if option == "Image Generator":

    st.header("🎨 AI Image Generator")
    prompt = st.text_input("Describe your image")

    if st.button("Generate Image"):
        if prompt.strip() == "":
            st.warning("Please enter a prompt")
        else:
            with st.spinner("Generating image..."):
                try:
                    # Clean the prompt string to make it safe for a URL endpoint
                    cleaned_prompt = requests.utils.quote(prompt)
                    
                    # Pollinations completely bypasses the need for an API key or bearer tokens!
                    image_url = f"https://image.pollinations.ai/p/{cleaned_prompt}?width=1024&height=1024&seed=42"
                    
                    response = requests.get(image_url, timeout=60)

                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(
                            image,
                            caption=f"Generated Image: '{prompt}'",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Image generation failed with status code: {response.status_code}")

                except requests.exceptions.Timeout:
                    st.error("The image generation request timed out. Please try again.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")
