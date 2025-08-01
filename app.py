import streamlit as st
from conversation_manager import ConversationManager

# Page Config
st.set_page_config(page_title="AI Multi-Model Chatbot", layout="wide")

# Title
st.title("🤖 AI Multi-Model Chatbot")
st.caption("Powered by Groq (default), OpenAI & Gemini")

# Initialize session state
if "manager" not in st.session_state:
    st.session_state.manager = ConversationManager(api_provider="groq")

manager = st.session_state.manager

# Sidebar
st.sidebar.header("⚙️ Settings")
api_provider = st.sidebar.selectbox("Choose API", ["Groq", "OpenAI", "Gemini"])
manager.api_provider = api_provider.lower()

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 300)

persona = st.sidebar.selectbox("Persona", ["Friendly", "Sarcastic", "Formal", "Custom"])
if persona == "Custom":
    custom_message = st.sidebar.text_area("Enter Custom Persona")
    if st.sidebar.button("Set Custom Persona"):
        manager.set_custom_system_message(custom_message)
else:
    manager.set_persona(persona)

if st.sidebar.button("Reset Conversation"):
    manager.reset_conversation_history()

# Show Current API in Main UI
api_colors = {
    "groq": "#22c55e",   # Green
    "openai": "#3b82f6", # Blue
    "gemini": "#f97316"  # Orange
}

st.markdown(
    f"""
    <div style='padding:10px; border-radius:8px; background-color:{api_colors[manager.api_provider]}; color:white; font-weight:bold;'>
        🚀 Currently using: {api_provider}
    </div>
    """,
    unsafe_allow_html=True
)

# Chat Interface
st.subheader("💬 Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in manager.display_history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                api_used = msg.get("api", manager.api_provider)
                st.markdown(
                    f"""
                    <div style='display:flex; align-items:center;'>
                        <span>{msg["content"]}</span>
                        <span style='margin-left:8px; padding:2px 6px; border-radius:5px; background:{api_colors.get(api_used, "#555")}; color:white; font-size:10px;'>
                            {api_used.capitalize()}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(msg["content"])


# Handle new user input
user_input = st.chat_input("Type your message...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    reply = manager.chat_completion(user_input, temperature, max_tokens)
    with st.chat_message("assistant"):
        api_used = manager.api_provider  # API just used
        st.markdown(
            f"""
            <div style='display:flex; align-items:center;'>
                <span>{reply}</span>
                <span style='margin-left:8px; padding:2px 6px; border-radius:5px; background:{api_colors.get(api_used, "#555")}; color:white; font-size:10px;'>
                    {api_used.capitalize()}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
