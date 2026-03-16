import streamlit as st
from chatbot.chatbot_logic import chatbot_response

def main():
    st.title("🤖 UrbanGuard - Smart City AI Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask about traffic, air quality, accidents, crowd, complaints...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 1. Get real data from AWS
            response = chatbot_response(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
