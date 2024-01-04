import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key='AIzaSyAkcjlhbaozHc0dMjK71JJEwX7TO_gIUHw')
model=genai.GenerativeModel('gemini-pro')

if "chat" not in st.session_state:
    st.session_state.chat=model.start_chat(history=[])

st.title("Chat with Google Gemini Pro")

def role_to_stream(role):
    if role=='model':
        return 'assistant'
    else:
        return role

for message in st.session_state.chat.history:
    with st.chat_message(role_to_stream(message.role)):
        st.markdown(message.parts[0].text)

if prompt := st.chat_input("I possess a well of knowledge.What would you like to know?"):
    st.chat_message("user").markdown(prompt)
    respone=st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(respone.text)