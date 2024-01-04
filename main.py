import streamlit as st
import google.generativeai as genai
import speech_recognition as sr

genai.configure(api_key='AIzaSyAkcjlhbaozHc0dMjK71JJEwX7TO_gIUHw')
model = genai.GenerativeModel('gemini-pro')

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

st.title("Chat with Google Gemini Pro")

def role_to_stream(role):
    return 'assistant' if role == 'model' else role

for message in st.session_state.chat.history:
    with st.chat_message(role_to_stream(message.role)):
        st.markdown(message.parts[0].text)

def getVoiceInput():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.success('Listening to Microphone')
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.warning('Speech Recognition could not understand audio.')
        except sr.RequestError as e:
            st.error(f'Could not request results from Google Speech Recognition service; {e}')
        return ""

if st.button('Click here to speak'):
    voiceInput = getVoiceInput()
    if voiceInput:
        st.chat_message("user").markdown(voiceInput)
        response = st.session_state.chat.send_message(voiceInput)
        with st.chat_message("assistant"):
            st.markdown(response.text)

if prompt := st.chat_input("I possess a well of knowledge.What would you like to know?"):
    st.chat_message("user").markdown(prompt)
    respone=st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(respone.text)
