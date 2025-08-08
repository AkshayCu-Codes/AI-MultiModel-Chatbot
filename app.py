import streamlit as st
import time
from conversation_manager import ConversationManager

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(page_title="AI Multi-Model Chatbot", layout="wide")

# ----------------------------
# Embedded CSS - OpenAI-like UI
# ----------------------------
st.markdown(
    """
    <style>
    :root{
        --bg: #0b1020; /* dark background (keeps your dark theme) */
        --panel: #0f1724;
        --card: #0b1220;
        --muted: #9aa4b2;
        --accent: #ff6b6b;
        --bubble-user: #2b3440;
        --bubble-assistant: transparent;
    }

    /* page background & container */
    .page {
        background: var(--bg);
        padding: 24px 24px;
    }
    .app-container {
        display:flex;
        gap:24px;
        align-items:stretch;
    }

    /* Left sidebar (we leave Streamlit sidebar as-is but style main area) */
    .main-panel {
        flex:1;
        max-width: 1100px;
        margin: 0 auto;
        color: #e6eef8;
        font-family: "Inter", "Segoe UI", Roboto, sans-serif;
    }

    /* header */
    .chat-header {
        margin-bottom: 18px;
    }
    .chat-title {
        font-size: 34px;
        font-weight: 700;
        margin: 6px 0;
    }
    .chat-sub {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 12px;
    }

    /* chat area card */
    .chat-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.6);
        border: 1px solid rgba(255,255,255,0.03);
        min-height: 60vh;
    }

    /* message list */
    .messages { display:flex; flex-direction:column; gap:12px; max-height:60vh; overflow:auto; padding-right:8px; }

    /* message row */
    .row { display:flex; gap:12px; align-items:flex-start; }
    .row.user { justify-content:flex-end; }
    .row.assistant { justify-content:flex-start; }

    /* avatar */
    .avatar {
        width:40px; height:40px; border-radius:50%; object-fit:cover; flex: 0 0 auto;
        box-shadow: 0 4px 12px rgba(2,6,23,0.6);
    }

    /* bubble-like blocks (kept minimal like OpenAI) */
    .msg {
        background: rgba(255,255,255,0.02);
        color: #e6eef8;
        padding: 12px 14px;
        border-radius: 10px;
        max-width: 78%;
        line-height:1.45;
        box-shadow: 0 2px 8px rgba(2,6,23,0.6);
    }
    .msg.user { background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); color: #e6eef8; }
    .msg.assistant { background: transparent; color: #e6eef8; }

    /* subtle API pill under message */
    .api-pill { margin-top:6px; font-size:11px; color:var(--muted); }

    /* sticky input area (OpenAI-like) */
    .input-bar {
        margin-top:14px;
        display:flex;
        align-items:center;
        gap:10px;
        padding:12px;
        border-radius:999px;
        background: linear-gradient(90deg, rgba(255,255,255,0.012), rgba(255,255,255,0.008));
        border: 1px solid rgba(255,255,255,0.03);
    }
    .input-text {
        flex:1;
        padding:10px 14px;
        border-radius:999px;
        background: transparent;
        color: #e6eef8;
        border: none;
        outline: none;
        font-size:15px;
    }
    .send-btn {
        background: linear-gradient(90deg,#ff7b7b,#ff5a9e);
        color:white;
        padding:10px 14px;
        border-radius:999px;
        border:none;
        cursor:pointer;
    }

    /* typing dots animation (pure CSS) */
    .typing-dots {
        display:inline-block;
        font-style:italic;
        color: var(--muted);
    }
    .typing-dots span {
        display:inline-block;
        animation: dot 1.4s infinite linear;
        margin-left:2px;
    }
    .typing-dots span:nth-child(1){ animation-delay:0s; }
    .typing-dots span:nth-child(2){ animation-delay:0.2s; }
    .typing-dots span:nth-child(3){ animation-delay:0.4s; }
    @keyframes dot {
        0% { transform: translateY(0); opacity:0.2; }
        50% { transform: translateY(-4px); opacity:1; }
        100% { transform: translateY(0); opacity:0.2; }
    }

    /* scrollbar styling inside messages */
    .messages::-webkit-scrollbar { width:8px; }
    .messages::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.03); border-radius: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Layout: keep Streamlit sidebar, style main content
# ----------------------------
st.markdown('<div class="page">', unsafe_allow_html=True)
st.markdown('<div class="app-container">', unsafe_allow_html=True)
st.markdown('<div class="main-panel">', unsafe_allow_html=True)

# Header
st.markdown('<div class="chat-header">', unsafe_allow_html=True)
st.markdown('<div class="chat-title">🤖 AI Multi-Model Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-sub">Powered by Groq, OpenAI & Gemini</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Initialize manager and session messages (exact same logic)
if "manager" not in st.session_state:
    st.session_state.manager = ConversationManager(api_provider="groq")
manager = st.session_state.manager

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls (unchanged functionality) - placed using Streamlit's built-in sidebar
st.sidebar.header("⚙️ Settings")
api_provider = st.sidebar.selectbox("Choose API", ["Groq", "OpenAI", "Gemini"])
manager.api_provider = api_provider.lower()

temperature = st.sidebar.slider(
    "Temperature",
    0.0, 1.0, 0.7,
    help="Controls creativity: Lower = more focused, Higher = more creative/random."
)
max_tokens = st.sidebar.slider(
    "Max Tokens",
    50, 500, 300,
    help="The maximum number of tokens (words + punctuation) in the model's reply."
)

persona = st.sidebar.selectbox("Persona", ["Friendly", "Sarcastic", "Formal", "Custom"])
if persona == "Custom":
    custom_message = st.sidebar.text_area("Enter Custom Persona")
    if st.sidebar.button("Set Custom Persona"):
        manager.set_custom_system_message(custom_message)
else:
    manager.set_persona(persona)

if st.sidebar.button("Reset Conversation"):
    manager.reset_conversation_history()
    st.session_state.messages = []

# Chat card / messages area
st.markdown('<div class="chat-card">', unsafe_allow_html=True)
st.markdown('<div class="messages" id="messages">', unsafe_allow_html=True)

# Display messages exactly as before, but wrapped in new styled HTML layout
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    role = msg["role"]
    avatar = "https://cdn-icons-png.flaticon.com/512/219/219970.png" if role == "user" else "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
    row_class = "row user" if role == "user" else "row assistant"
    bubble_class = "msg user" if role == "user" else "msg assistant"
    # Render row with avatar on correct side (we mimic OpenAI: user right, assistant left)
    if role == "assistant":
        st.markdown(
            f'''
            <div class="{row_class}">
                <img class="avatar" src="{avatar}" />
                <div>
                    <div class="{bubble_class}">{msg["content"]}</div>
                    <div class="api-pill">[{msg["api"]}]</div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'''
            <div class="{row_class}">
                <div style="flex:1"></div>
                <div>
                    <div class="{bubble_class}">{msg["content"]}</div>
                    <div class="api-pill">[{msg["api"]}]</div>
                </div>
                <img class="avatar" src="{avatar}" />
            </div>
            ''',
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)  # close messages

# Input area: keep using st.chat_input() for behavior, but show styled input UI and replace immediately
# We will use a hidden chat_input (to keep Streamlit behavior) and also provide a visible styled input for UX.
# We'll stick with st.chat_input to avoid changing functionality.

st.markdown(
    """
    <div style="height:8px"></div>
    """,
    unsafe_allow_html=True,
)

# Place a container for the typing placeholder and new replies to be swapped in-place.
typing_container = st.empty()

# Use the native st.chat_input (keeps behavior identical)
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message (exact same structure)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "api": api_provider
    })

    # Immediately show the user message in the UI (we do this by rerendering a mini row)
    # Note: We simply append to messages and rerun; here we proceed to show typing placeholder then call API.
    # Insert typing marker in UI using the last position: create a placeholder element we can overwrite.
    placeholder = typing_container.empty()
    # typing HTML with CSS animated dots (client-side animation)
    typing_html = '''
        <div class="row assistant">
          <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" />
          <div>
            <div class="msg assistant"><span class="typing-dots">Assistant is typing <span>.</span><span>.</span><span>.</span></span></div>
            <div class="api-pill">[{api}]</div>
          </div>
        </div>
    '''.replace("{api}", api_provider)
    placeholder.markdown(typing_html, unsafe_allow_html=True)

    # Call the model (blocking). While the blocking call runs, the browser will keep CSS animation running.
    reply = manager.chat_completion(user_input, temperature, max_tokens)

    # Replace typing placeholder with the assistant reply in the exact same spot
    reply_html = f'''
        <div class="row assistant">
          <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" />
          <div>
            <div class="msg assistant">{reply}</div>
            <div class="api-pill">[{api_provider}]</div>
          </div>
        </div>
    '''
    placeholder.markdown(reply_html, unsafe_allow_html=True)

    # Save to session messages (same as before)
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "api": api_provider
    })

st.markdown('</div>', unsafe_allow_html=True)  # close chat-card
st.markdown('</div>', unsafe_allow_html=True)  # close main-panel
st.markdown('</div>', unsafe_allow_html=True)  # close app-container
st.markdown('</div>', unsafe_allow_html=True)  # close page
