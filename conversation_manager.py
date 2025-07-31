import os
import groq
from openai import OpenAI as OpenAIClient
import google.generativeai as genai


class ConversationManager:
    def __init__(self, api_provider="groq"):
        self.api_provider = api_provider.lower()
        self.history = []
        self.persona_message = "You are a friendly AI chatbot."

        # API Keys from environment variables (Streamlit Secrets recommended)
        self.groq_client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))
        self.openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
        self.history = []

    def chat_completion(self, user_input, temperature=0.7, max_tokens=300):
        self.history.append({"role": "user", "content": user_input})

        try:
            if self.api_provider == "openai":
                return self._chat_openai(user_input, temperature, max_tokens)
            elif self.api_provider == "gemini":
                return self._chat_gemini(user_input, temperature, max_tokens)
            else:  # Default Groq
                return self._chat_groq(user_input, temperature, max_tokens)

        except Exception:
            # Fallback to Groq if other APIs fail
            return self._chat_groq(user_input, temperature, max_tokens)

    def _chat_groq(self, user_input, temperature, max_tokens):
        response = self.groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": self.persona_message},
                *self.history
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message["content"]
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def _chat_openai(self, user_input, temperature, max_tokens):
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.persona_message},
                *self.history
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        reply = response.choices[0].message["content"]
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def _chat_gemini(self, user_input, temperature, max_tokens):
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"{self.persona_message}\nUser: {user_input}")
        reply = response.text
        self.history.append({"role": "assistant", "content": reply})
        return reply