import streamlit as st
import groq
from openai import OpenAI as OpenAIClient
import google.generativeai as genai


class ConversationManager:
    def __init__(self, api_provider="groq"):
        self.api_provider = api_provider.lower()

        # API Keys from Streamlit secrets
        self.groq_api_key = st.secrets.get("GROQ_API_KEY")
        self.openai_api_key = st.secrets.get("OPENAI_API_KEY")
        self.gemini_api_key = st.secrets.get("GEMINI_API_KEY")

        # Initialize API clients
        self.openai_client = OpenAIClient(api_key=self.openai_api_key) if self.openai_api_key else None
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)

        # System message
        self.system_message = {"role": "system", "content": "You are a helpful assistant."}
        self.persona_message = self.system_message["content"]

        # Conversation history for API calls (API-safe format)
        self.conversation_history = [self.system_message]

        # Display history for UI (can store API info here)
        self.display_history = []  

    def set_persona(self, persona):
        personas = {
            "Friendly": "You are a friendly and helpful assistant.",
            "Sarcastic": "You respond with light sarcasm while still being helpful.",
            "Formal": "You respond in a formal, professional tone."
        }
        self.persona_message = personas.get(persona, self.persona_message)

    def set_custom_system_message(self, message):
        self.persona_message = message

    def reset_conversation_history(self):
        self.conversation_history = [self.system_message]
        self.display_history = []

    def chat_completion(self, user_input, temperature=0.7, max_tokens=300):
        # Append user message (API-safe)
        self.conversation_history.append({"role": "user", "content": user_input})
        self.display_history.append({"role": "user", "content": user_input})

        try:
            if self.api_provider == "openai":
                reply = self._chat_openai(user_input, temperature, max_tokens)
            elif self.api_provider == "gemini":
                reply = self._chat_gemini(user_input, temperature, max_tokens)
            else:
                reply = self._chat_groq(user_input, temperature, max_tokens)
        except Exception:
            reply = self._chat_groq(user_input, temperature, max_tokens)

        # Append assistant message to both histories
        self.conversation_history.append({"role": "assistant", "content": reply})
        self.display_history.append({"role": "assistant", "content": reply, "api": self.api_provider})

        return reply

    def _chat_groq(self, user_input, temperature, max_tokens):
        client = groq.Groq(api_key=self.groq_api_key)
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=self.conversation_history,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def _chat_openai(self, user_input, temperature, max_tokens):
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.persona_message},
                *self.conversation_history
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def _chat_gemini(self, user_input, temperature, max_tokens):
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"{self.persona_message}\nUser: {user_input}")
        return response.text
