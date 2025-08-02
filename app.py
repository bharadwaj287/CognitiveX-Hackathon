import streamlit as st
from utils.tone_rewriter import rewrite_text
from utils.tts_generator import get_available_voices, generate_audio, preview_voice
from utils.session_manager import save_narration

st.set_page_config(page_title="EchoVerse", layout="wide")
st.markdown("<style>" + open("assets/styles.css").read() + "</style>", unsafe_allow_html=True)

st.title("🎧 EchoVerse – AI-Powered Audiobook Creator")

# 📥 Input Section
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
input_text = st.text_area("Or paste your text here")

if uploaded_file:
    input_text = uploaded_file.read().decode("utf-8")

# 🎭 Tone and Voice Selection
tone = st.selectbox("Select Tone", ["Neutral", "Suspenseful", "Inspiring"])

voices = get_available_voices()
voice_names = [v["display"] for v in voices]
selected_voice_display = st.selectbox("Choose a voice", voice_names)
selected_voice_id = next(v["id"] for v in voices if v["display"] == selected_voice_display)

# 🔊 Preview Voice
if st.button("🔊 Preview Voice"):
    preview_audio = preview_voice(selected_voice_id)
    st.audio(preview_audio, format="audio/mp3")

# 🎙️ Rewrite and Generate Narration
if st.button("Generate Audiobook") and input_text:
    with st.spinner("Rewriting text..."):
        rewritten = rewrite_text(input_text, tone)

    with st.spinner("Synthesizing Audio..."):
        audio_bytes = generate_audio(rewritten, selected_voice_id)

    save_narration(rewritten, tone, selected_voice_display, audio_bytes)

    # 📝 Display Original vs Rewritten
    col1, col2 = st.columns(2)
    col1.subheader("Original Text")
    col1.write(input_text)
    col2.subheader("Rewritten Text")
    col2.write(rewritten)

    # 🔈 Audio Playback + Download
    st.subheader("🔈 Preview Narration")
    st.audio(audio_bytes, format="audio/wav")
    st.download_button("Download Narration", data=audio_bytes, file_name="narration.wav")

# 📜 Past Narrations
if "narrations" in st.session_state:
    with st.expander("📜 Past Narrations"):
        for i, item in enumerate(st.session_state.narrations):
            st.write(f"**Narration {i+1}** – Tone: {item['tone']}, Voice: {item['voice']}")
            st.write(item["text"])
            st.audio(item["audio"], format="audio/mp3")
            st.download_button(f"Download Narration {i+1}", data=item["audio"], file_name=f"narration_{i+1}.mp3")
