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
if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"]
else:
    groq_key = ""

# ======================================
# SIDEBAR
# ======================================
option = st.sidebar.selectbox(
    "Choose Feature",
    ["Chatbot", "Image Generator"]
)

# ======================================
# 💬 CHATBOT FEATURE (ChatGPT Interface Style)
# ======================================
if option == "Chatbot":

    st.header("💬 AI Chatbot")
    
    if not groq_key:
        st.warning("⚠️ Please add your `GROQ_API_KEY` to your Streamlit Secrets panel to use the chatbot.")
    
    # Text input field for user prompts
    user_input = st.text_input("Message Chatbot...", placeholder="Ask me anything...", key="chat_input")

    if st.button("Send Message", use_container_width=True):
        if user_input.strip() == "":
            st.warning("Please enter a message first!")
        elif not groq_key:
            st.error("Missing API Key configuration.")
        else:
            # 1. Render User Message Bubble
            with st.chat_message("user"):
                st.write(user_input)
                
            # 2. Compute and Render Assistant Message Bubble
            with st.spinner("Thinking..."):
                try:
                    client = Groq(api_key=groq_key)
                    
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    
                    response_text = completion.choices[0].message.content
                    
                    # Render sleek Chatbot Response Bubble
                    with st.chat_message("assistant"):
                        st.write(response_text)

                except Exception as e:
                    st.error(f"Chatbot failed to respond: {e}")

# ======================================
# 🎨 IMAGE GENERATOR FEATURE
# ======================================
if option == "Image Generator":

    st.header("🎨 AI Image Generator")
    prompt = st.text_input("Describe the image you want to create...")

    if st.button("Generate Image", use_container_width=True):
        if prompt.strip() == "":
            st.warning("Please enter a description prompt.")
        else:
            with st.spinner("Generating image..."):
                try:
                    cleaned_prompt = requests.utils.quote(prompt)
                    image_url = f"https://image.pollinations.ai/p/{cleaned_prompt}?width=1024&height=1024&seed=42"
                    
                    response = requests.get(image_url, timeout=60)

                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        st.image(
                            image,
                            caption=f"Generated Layout: '{prompt}'",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Generation stopped. Status code: {response.status_code}")

                except requests.exceptions.Timeout:
                    st.error("The network request timed out. Please try running it again.")
                except Exception as e:
                    st.error(f"Error fetching image: {e}")
