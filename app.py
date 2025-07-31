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

# Chat Interface
st.subheader("💬 Chat")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in manager.history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    reply = manager.chat_completion(user_input, temperature, max_tokens)
    with st.chat_message("assistant"):
        st.markdown(reply)
