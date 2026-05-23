import streamlit as st

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="EcoBin GPT",
    page_icon="♻️",
    layout="wide"
)

# ======================================
# CUSTOM CSS
# ======================================

st.markdown("""
<style>

.stApp {
    background-color: #343541;
    color: white;
}

.chat-container {
    max-width: 900px;
    margin: auto;
}

.user-message {
    background-color: #0b93f6;
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    color: white;
    text-align: right;
}

.bot-message {
    background-color: #444654;
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    color: white;
}

.stTextInput input {
    background-color: #40414f;
    color: white;
    border-radius: 10px;
}

.stButton button {
    background-color: #19c37d;
    color: white;
    border-radius: 10px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# TITLE
# ======================================

st.title("♻️ EcoBin GPT")
st.caption("Smart Waste Management Assistant")

# ======================================
# SESSION STATE
# ======================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================
# USER INPUT
# ======================================

user_input = st.chat_input(
    "Ask EcoBin anything about waste management..."
)

# ======================================
# PROCESS USER INPUT
# ======================================

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    message = user_input.lower()

    # ======================================
    # BOT RESPONSES
    # ======================================

    if "hello" in message or "hi" in message:
        bot_response = "Hello! Welcome to EcoBin GPT."
        image_prompt = "eco friendly smart waste management"

    elif "plastic" in message:
        bot_response = (
            "Plastic waste should go into the recyclable bin."
        )
        image_prompt = "plastic recycling bin"

    elif "paper" in message:
        bot_response = (
            "Paper waste is recyclable if it is clean and dry."
        )
        image_prompt = "paper recycling waste"

    elif "glass" in message:
        bot_response = (
            "Glass bottles and jars can be recycled safely."
        )
        image_prompt = "glass bottle recycling"

    elif "metal" in message:
        bot_response = (
            "Metal cans are recyclable and reusable."
        )
        image_prompt = "metal waste recycling"

    elif "organic" in message or "food" in message:
        bot_response = (
            "Organic waste can be composted into fertilizer."
        )
        image_prompt = "organic compost waste"

    elif "recycle" in message:
        bot_response = (
            "Recycling helps reduce pollution and save resources."
        )
        image_prompt = "green recycling environment"

    elif "smart bin" in message:
        bot_response = (
            "Smart bins use sensors and AI to monitor waste levels."
        )
        image_prompt = "smart ai trash bin"

    elif "benefits" in message:
        bot_response = (
            "EcoBin improves waste segregation and cleanliness."
        )
        image_prompt = "clean green smart city"

    elif "bye" in message:
        bot_response = (
            "Goodbye! Keep the environment clean and green."
        )
        image_prompt = "green earth environment"

    else:
        bot_response = (
            "Sorry, I do not understand that yet."
        )
        image_prompt = "waste management"

    # Save bot message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_response,
            "image": image_prompt
        }
    )

# ======================================
# DISPLAY CHAT HISTORY
# ======================================

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message("user"):
            st.markdown(msg["content"])

    else:

        with st.chat_message("assistant"):

            st.markdown(msg["content"])

            # Generate AI image
            image_url = (
                f"https://image.pollinations.ai/prompt/{msg['image']}"
            )

            st.image(
                image_url,
                use_container_width=True
            )

            st.markdown(
                f"[Download Image]({image_url})"
            )

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.header("🌱 Eco Tips")

    st.success(
        "Segregate biodegradable and recyclable waste."
    )

    st.success(
        "Reduce single-use plastics."
    )

    st.success(
        "Recycle paper, glass, and metal properly."
    )

    st.success(
        "Compost food waste whenever possible."
    )

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
