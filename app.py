from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import json

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set page configuration
st.set_page_config(page_title="✨ StarChat LLM", page_icon="🌠", layout="wide")

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
if 'chat' not in st.session_state:
    st.session_state['chat'] = model.start_chat(history=[])

def get_gemini_response(question):
    chat = st.session_state['chat']
    response = chat.send_message(question, stream=True)
    return response

# Function to save chat history to a file
def save_chat_history(filename="chat_history.json"):
    with open(filename, 'w') as file:
        json.dump(st.session_state['chat_history'], file)

# Function to load chat history from a file
def load_chat_history(filename="chat_history.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            st.session_state['chat_history'] = json.load(file)

# Add custom CSS and JS for improved UI
st.markdown("""
    <style>
    /* Overall page styling */
    body {
        background: linear-gradient(to right, #fc466b, #3f5efb); /* Vibrant background gradient */
        font-family: 'Verdana', sans-serif;
        color: #fff; /* Default text color */
    }

    /* Top navigation bar styling */
    .nav-bar {
        background-color: #343a40;
        padding: 10px 20px;
        color: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
    }

    .nav-bar a {
        color: #ffffff;
        text-decoration: none;
        padding: 8px 15px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    .nav-bar a:hover {
        background-color: #495057;
    }

    .nav-bar .menu-links {
        display: flex;
    }

    /* Chat message box styling */
    .message-box {
        background: linear-gradient(to bottom, #ffffff, #e0e0e0);
        border-radius: 12px;
        padding: 10px 15px;
        margin: 10px;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        color: #333;
    }
    .message-box.user {
        background: linear-gradient(to right, #34e89e, #0f3443);
        color: #fff;
    }
    .message-box.bot {
        background: linear-gradient(to right, #e66465, #9198e5);
        color: #fff;
    }

    /* Input and button styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #6c757d;
        border-radius: 8px;
        padding: 10px;
        font-size: 1.1em;
        color: #333;
    }

    .stButton > button {
        background-color: #343a40;
        color: #ffffff;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1.1em;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #495057;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Render the top navigation menu
st.markdown("""
    <div class="nav-bar">
        <div><strong>🌠 StarChat Navigation</strong></div>
        <div class="menu-links">
            <a href="#">Home</a>
            <a href="#">Features</a>
            <a href="#">Settings</a>
            <a href="#">About</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main UI header
st.header("Welcome to StarChat 🌟 Your AI Companion")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input section
input_text = st.text_input("Ask me anything 🤔", key="input")
submit = st.button("Send 🚀")

# Buttons to save and load chat history
col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save Chat"):
        save_chat_history()
        st.success("Chat history saved successfully!")
with col2:
    if st.button("📂 Load Chat"):
        load_chat_history()
        st.success("Chat history loaded successfully!")

# Display the chat responses when the user submits a question
if submit and input_text:
    response = get_gemini_response(input_text)
    
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("🧑", input_text))
    
    bot_response = ""
    st.subheader("The Response is 💬")
    
    for chunk in response:
        if hasattr(chunk, 'text'):
            st.write(chunk.text)
            bot_response += chunk.text + " "
        else:
            bot_response = "Sorry, I couldn't process your request."
    
    # Add the bot's response to chat history
    st.session_state['chat_history'].append(("🤖", bot_response.strip()))

# Display the chat history with updated styling
st.subheader("Chat History 📜")
chat_history_container = st.container()

with chat_history_container:
    for role, text in st.session_state['chat_history']:
        css_class = "user" if role == "🧑" else "bot"
        st.markdown(f'<div class="message-box {css_class}"><b>{role}:</b> {text}</div>', unsafe_allow_html=True)
