from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# Configure the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model and start a chat session
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    context = "This question is about Rangsit University in Thailand: "
    full_question = context + question
    response = chat.send_message(full_question, stream=True)
    response.resolve()  # Ensure complete loading of the response
    return response.text  # Adjust based on the actual response structure

# Streamlit app setup
st.set_page_config(page_title="Rangsit University Chatbot", layout="wide")
st.title("Rangsit University Assistant")

# Explicitly initialize chat_history and chat_visibility in session state if they don't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'chat_visibility' not in st.session_state:
    st.session_state['chat_visibility'] = True

# Sidebar for chat history visibility toggle
with st.sidebar:
    st.header("Controls")
    if st.button("Toggle Chat History"):
        st.session_state['chat_visibility'] = not st.session_state['chat_visibility']

# Container for input and immediate feedback
with st.container():
    with st.form(key='question_form', clear_on_submit=True):
        input = st.text_input("Ask me anything about Rangsit University:", value='')
        submit = st.form_submit_button(label='Ask')
    
    if submit and input:
        with st.spinner('Fetching your answer...'):
            response_text = get_gemini_response(input)
        st.session_state['chat_history'].append(("You", input))
        st.markdown(f"**Bot:** {response_text}", unsafe_allow_html=True)
        st.session_state['chat_history'].append(("Bot", response_text))

# Conditionally display chat history based on the toggle state
if st.session_state['chat_visibility']:
    with st.sidebar:
        st.header("Chat History")
        for role, text in st.session_state.get('chat_history', []):
            st.markdown(f"**{role}:** {text}", unsafe_allow_html=True)
