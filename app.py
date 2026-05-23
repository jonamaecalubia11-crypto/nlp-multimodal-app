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

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #22c55e;
    text-align: center;
}

.stButton button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# TITLE
# ======================================

st.title("♻️ EcoBin AI Assistant")
st.subheader("Smart Waste Management Chatbot + AI Image Generator")

# ======================================
# USER INPUT
# ======================================

user_input = st.text_input(
    "Ask about waste management"
)

# ======================================
# PROCESS
# ======================================

if st.button("Send"):

    if user_input.strip() == "":
        st.warning("Please enter a message")

    else:

        message = user_input.lower()

        # ======================================
        # CHATBOT RESPONSES
        # ======================================

        if "hello" in message or "hi" in message:
            response = "Hello! Welcome to EcoBin AI Assistant."
            image_prompt = "eco friendly smart waste management"

        elif "plastic" in message:
            response = "Plastic waste should go into the recyclable bin."
            image_prompt = "plastic waste recycling bin"

        elif "paper" in message:
            response = "Paper waste is recyclable if it is clean and dry."
            image_prompt = "paper recycling waste"

        elif "glass" in message:
            response = "Glass bottles and jars can be recycled safely."
            image_prompt = "glass bottle recycling"

        elif "metal" in message:
            response = "Metal cans are recyclable and reusable."
            image_prompt = "metal waste recycling"

        elif "organic" in message or "food" in message:
            response = "Organic waste can be composted into fertilizer."
            image_prompt = "organic compost waste"

        elif "recycle" in message:
            response = "Recycling helps reduce pollution and save resources."
            image_prompt = "recycling environment"

        elif "smart bin" in message:
            response = "Smart bins use sensors and AI to monitor waste levels."
            image_prompt = "smart ai trash bin"

        elif "benefits" in message:
            response = "EcoBin improves waste segregation and cleanliness."
            image_prompt = "clean green environment"

        elif "bye" in message:
            response = "Goodbye! Keep the environment clean and green."
            image_prompt = "green earth clean environment"

        else:
            response = "Sorry, I do not understand that yet."
            image_prompt = "waste management"

        # ======================================
        # DISPLAY CHATBOT RESPONSE
        # ======================================

        st.success(response)

        # ======================================
        # GENERATE AI IMAGE
        # ======================================

        with st.spinner("Generating AI image..."):

            image_url = (
                f"https://image.pollinations.ai/prompt/{image_prompt}"
            )

            st.image(
                image_url,
                caption="EcoBin AI Generated Image",
                use_container_width=True
            )

            st.markdown(
                f"[Download Image]({image_url})"
            )

# ======================================
# ECO TIPS
# ======================================

st.divider()

st.header("🌱 Eco Tips")

tips = [
    "Use reusable bags instead of plastic bags.",
    "Segregate biodegradable and recyclable waste.",
    "Reduce single-use plastics.",
    "Recycle paper, glass, and metal properly.",
    "Compost food waste whenever possible."
]

for tip in tips:
    st.info(tip)
