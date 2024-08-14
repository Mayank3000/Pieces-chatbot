import streamlit as st
from pieces_copilot_sdk import PiecesClient

# Initialize PiecesClient
pieces_client = PiecesClient(
    config={
        'baseUrl': 'http://localhost:1000'
    }
)

# Set the page layout and title
st.set_page_config(layout="wide", page_title="AI Chatbot")

# Initialize session state for chat history and user input
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Display the chat interface
st.title("AI Chatbot Interface")

# Text input for the user to ask questions
user_input = st.text_input("Ask: ", value=st.session_state.user_input, key="input")
if st.button("Send"):
    if user_input:
        # Add user query to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # Get response from PiecesClient
        try:
            response = pieces_client.ask_question(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {str(e)}"})
        # Clear input after submission
        st.session_state.user_input = ""

#Display the chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(
            f'<div style="text-align: right; background-color: #e1ffc7; border-radius: 10px; padding: 10px; margin-bottom: 10px; max-width: 80%; display: inline-block; color: black;">{chat["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="text-align: left; background-color: #ffffff; border-radius: 10px; padding: 10px; margin-bottom: 10px; max-width: 80%; display: inline-block; color: black;">{chat["content"]}</div>',
            unsafe_allow_html=True
        )

#Clear chat history button
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    # Clearing input for a fresh start
    st.session_state.user_input = ""
