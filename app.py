from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Set the page configuration at the very beginning
st.set_page_config(page_title="💬 Gemini QA Bot", page_icon="🤖")

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Function to load Gemini Pro model and get response
model = genai.GenerativeModel("gemini-pro")
if 'chat' not in st.session_state:
    st.session_state['chat'] = model.start_chat(history=[])

def get_gemini_response(question):
    chat = st.session_state['chat']
    response = chat.send_message(question, stream=True)
    return response

# Add custom CSS and JS
st.markdown("""
    <style>
    /* Custom font and background */
    body {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        background: linear-gradient(135deg, #f3f3f3, #f7f7f7);
    }
    /* Header styling */
    .stApp h1 {
        color: #ff6347;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    /* Input box styling */
    .stTextInput > div > div > input {
        background-color: #ffecd1;
        font-size: 1.2em;
        border: 2px solid #ff6347;
        border-radius: 10px;
        padding: 10px;
    }
    /* Button styling with animation */
    .stButton > button {
        background-color: #ff6347;
        color: white;
        font-size: 1.2em;
        border-radius: 10px;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #ff4500;
        transform: scale(1.1);
    }
    /* Chat history styling */
    .stApp .chat-history {
        background-color: #fff4e6;
        border: 2px solid #ff6347;
        border-radius: 10px;
        padding: 15px;
        margin-top: 1rem;
        max-height: 300px;
        overflow-y: auto;
    }
    /* Emoji styling */
    .emoji {
        font-size: 1.5em;
        margin-right: 5px;
    }
    </style>

    <script>
    // Custom JS for animations or effects
    document.addEventListener("DOMContentLoaded", function() {
        let header = document.querySelector('.stApp h1');
        header.style.opacity = 0;
        header.style.transition = "opacity 2s ease-in-out";
        setTimeout(() => {
            header.style.opacity = 1;
        }, 100);
    });
    </script>
""", unsafe_allow_html=True)

# Initialize our Streamlit app with a new header
st.header("Welcome to Gemini LLM Application 💡")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("What's your question? 🤔", key="input")
submit = st.button("Ask the Question 🚀")

if submit and input_text:
    response = get_gemini_response(input_text)
    
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    
    bot_response = ""
    st.subheader("The Response is 🌟")
    
    for chunk in response:
        if hasattr(chunk, 'text'):
            st.write(chunk.text)
            bot_response += chunk.text + " "
        else:
            bot_response = "The response was blocked or invalid."
    
    # Add the bot's response to chat history
    st.session_state['chat_history'].append(("Bot", bot_response.strip()))

st.subheader("Your Chat History 📜")
chat_history_container = st.container()

# Add a div with class 'chat-history' to apply custom styling
with chat_history_container:
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for role, text in st.session_state['chat_history']:
        st.write(f"**{role}:** {text}")
    st.markdown('</div>', unsafe_allow_html=True)
