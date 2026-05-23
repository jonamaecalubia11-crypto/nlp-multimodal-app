import streamlit as st
import requests
from groq import Groq
from PIL import Image
from io import BytesIO

# ======================================
# PAGE CONFIGURATION & LAYOUT
# ======================================
st.set_page_config(page_title="Gemini-Style AI Assistant", layout="centered")

st.title("✨ Gemini-Style AI Assistant")
st.subheader("Chatbot and Image Generation in one timeline")

# ======================================
# SECRETS CONFIGURATION
# ======================================
if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"]
else:
    groq_key = ""

# Show a warning if the API key is missing
if not groq_key:
    st.warning("⚠️ Please add your `GROQ_API_KEY` to your Streamlit Secrets panel to enable the Chatbot.")

# ======================================
# INITIALIZE CHAT HISTORY (Memory)
# ======================================
# This prevents your history from disappearing when you press buttons
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "type": "text", "content": "Hello! I am your Gemini-style assistant. Ask me a question, or tell me to generate an image!"}
    ]

# ======================================
# RENDER ALL PAST MESSAGES FROM MEMORY
# ======================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            # Re-fetch image from bytes or pass the PIL object directly if stored
            st.image(msg["content"], use_container_width=True)

# ======================================
# THE UNIFIED CHAT INPUT (The Gemini Box)
# ======================================
if user_input := st.chat_input("Ask a question or type 'generate an image of...'"):
    
    # 1. Instantly display user's prompt in the timeline and save to memory
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "type": "text", "content": user_input})

    # 2. Check intent: Did the user ask for an image?
    image_keywords = ["generate", "draw", "paint", "create an image", "image of", "picture of", "sketch"]
    is_image_request = any(keyword in user_input.lower() for keyword in image_keywords)

    # ----------------------------------
    # BRANCH A: IMAGE GENERATION INTENT
    # ----------------------------------
    if is_image_request:
        with st.chat_message("assistant"):
            with st.spinner("Generating your image..."):
                try:
                    # Clean the prompt for the URL query string
                    cleaned_prompt = requests.utils.quote(user_input)
                    image_url = f"https://image.pollinations.ai/p/{cleaned_prompt}?width=1024&height=1024&seed=42"
                    
                    response = requests.get(image_url, timeout=60)

                    if response.status_code == 200:
                        image_data = Image.open(BytesIO(response.content))
                        
                        # Display inside the live message box
                        st.image(image_data, use_container_width=True)
                        
                        # Save the image object directly into memory history
                        st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_data})
                    else:
                        st.error(f"Failed to generate image. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Error creating image: {e}")

    # ----------------------------------
    # BRANCH B: TEXT CHATBOT INTENT
    # ----------------------------------
    else:
        with st.chat_message("assistant"):
            if not groq_key:
                st.error("Cannot reply. Missing GROQ_API_KEY in Secrets.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        client = Groq(api_key=groq_key)
                        
                        # Convert session state memory to Groq model API format
                        api_messages = []
                        for m in st.session_state.messages:
                            if m["type"] == "text":  # Groq only accepts text strings
                                api_messages.append({"role": m["role"], "content": m["content"]})

                        completion = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=api_messages,
                            temperature=0.7,
                            max_tokens=1024,
                        )
                        
                        response_text = completion.choices[0].message.content
                        
                        # Display response text and save to memory history
                        st.write(response_text)
                        st.session_state.messages.append({"role": "assistant", "type": "text", "content": response_text})
                        
                    except Exception as e:
                        st.error(f"Chatbot processing failed: {e}")
