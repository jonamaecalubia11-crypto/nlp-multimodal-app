import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ======================================
# PAGE SETTINGS
# ======================================

st.set_page_config(page_title="NLP Multi-Modal AI App")

st.title("🤖 NLP Multi-Modal AI App")
st.subheader("Chatbot + AI Image Generator")

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

            with st.spinner("Thinking..."):

                try:

                    url = f"https://api.affiliateplus.xyz/api/chatbot?message={user_input}&botname=NLPBot&ownername=Jona"

                    response = requests.get(url)

                    data = response.json()

                    reply = data["message"]

                    st.success(reply)

                except Exception as e:
                    st.error(f"Error: {e}")

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
