import streamlit as st

def save_narration(text, tone, voice, audio_bytes):
    if "narrations" not in st.session_state:
        st.session_state.narrations = []
    st.session_state.narrations.append({
        "text": text,
        "tone": tone,
        "voice": voice,
        "audio": audio_bytes
    })
