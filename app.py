import streamlit as st

# ======================================
# PAGE SETTINGS
# ======================================

st.set_page_config(
    page_title="EcoBin AI Assistant",
    page_icon="♻️",
    layout="centered"
)

# ======================================
# CUSTOM STYLE
# ======================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }

    h1, h2, h3 {
        color: #22c55e;
    }

    .stButton button {
        background-color: #22c55e;
        color: white;
        border-radius: 10px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================
# TITLE
# ======================================

st.title("♻️ EcoBin AI Assistant")
st.subheader("Smart Waste Management System")

# ======================================
# SIDEBAR
# ======================================

option = st.sidebar.selectbox(
    "Choose Feature",
    ["EcoBin Chatbot", "Waste Image Generator"]
)

# ======================================
# CHATBOT
# ======================================

if option == "EcoBin Chatbot":

    st.header("💬 EcoBin Chatbot")

    user_input = st.text_input(
        "Ask about waste management"
    )

    if st.button("Send"):

        if user_input.strip() == "":
            st.warning("Please enter a message")

        else:

            message = user_input.lower()

            # NLP responses
            if "hello" in message or "hi" in message:
                response = "Hello! Welcome to EcoBin AI Assistant."

            elif "plastic" in message:
                response = "Plastic waste should be placed in the recyclable bin."

            elif "paper" in message:
                response = "Paper waste is recyclable and should stay dry."

            elif "glass" in message:
                response = "Glass bottles and jars can be recycled safely."

            elif "metal" in message:
                response = "Metal cans are recyclable and reusable."

            elif "organic" in message or "food" in message:
                response = "Organic waste can be composted for fertilizer."

            elif "recycle" in message:
                response = "Recycling helps reduce pollution and save resources."

            elif "ecobin" in message:
                response = "EcoBin is a smart waste management system using AI and NLP."

            elif "smart bin" in message:
                response = "Smart bins use sensors and AI to monitor waste levels."

            elif "benefits" in message:
                response = "EcoBin helps improve waste segregation and environmental awareness."

            elif "bye" in message:
                response = "Goodbye! Keep the environment clean and green."

            else:
                response = "Sorry, I do not understand that yet."

            st.success(response)

# ======================================
# IMAGE GENERATOR
# ======================================

elif option == "Waste Image Generator":

    st.header("🎨 Waste Image Generator")

    prompt = st.text_input(
        "Describe waste image"
    )

    if st.button("Generate Image"):

        if prompt.strip() == "":
            st.warning("Please enter a prompt")

        else:

            with st.spinner("Generating image..."):

                image_url = (
                    f"https://image.pollinations.ai/prompt/{prompt}"
                )

                st.image(
                    image_url,
                    caption="Generated Waste Image",
                    use_container_width=True
                )

                st.markdown(
                    f"[Download Image]({image_url})"
                )

* User login system
* Database storage
