# 🤖 AI Multi-Model Chatbot  


An AI chatbot built with **Streamlit** supporting multiple AI models:  
- **Groq** (LLaMA-3-8B, free default)  
- **OpenAI** (GPT-3.5 / GPT-4o)  
- **Google Gemini** (Gemini 1.5 Flash)  

---

## 🚀 Features  
- Switch between **Groq**, **OpenAI**, and **Gemini**  
- **Personas**: Friendly, Sarcastic, Formal, Custom  
- Adjustable **temperature** and **token limits**  
- **Reset conversation** button  
- Automatic **fallback to Groq** if other APIs fail  

---

## 📸 Screenshots  
![Chatbot Screenshot](assets/screenshot1.png)  
![Persona Settings](assets/screenshot2.png)  

---

## 🔧 Installation  
```bash
git clone https://github.com/YOUR-USERNAME/AI-MultiModel-Chatbot.git  
cd AI-MultiModel-Chatbot  
pip install -r requirements.txt  
```

## 🔑 API Keys Setup  
Create a file at .streamlit/secrets.toml with:

```toml
GROQ_API_KEY = "your_groq_key"  
OPENAI_API_KEY = "your_openai_key"  
GEMINI_API_KEY = "your_gemini_key"  
```
## ▶️ Run Locally
```bash
streamlit run app.py
```
## ☁️ Deploy on Streamlit Cloud
Push this repo to GitHub  
Go to Streamlit Cloud  
Connect your repo & set API keys in Secrets  
Click Deploy 🚀  

## 📜 License
MIT License



---

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Deploy Streamlit](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-orange?logo=streamlit)](https://share.streamlit.io)  
