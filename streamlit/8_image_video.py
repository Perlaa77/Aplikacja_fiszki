import streamlit as st

st.set_page_config(
    page_title = "Przykład 8"
)

st.subheader("Obraz")
uploaded_image = st.file_uploader("Wgraj obraz (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])
if uploaded_image:
    st.image(uploaded_image, caption="Twój obraz") # Zamiast uploaded_image można także wpisać ścieżkę do pliku

st.subheader("Wideo")
uploaded_video = st.file_uploader("Wgraj plik wideo (mp4)", type=["mp4"])
if uploaded_video:
    st.video(uploaded_video)

st.subheader("Audio")
uploaded_audio = st.file_uploader("Wgraj plik audio (mp3, wav)", type=["mp3", "wav"])
if uploaded_audio:
    st.audio(uploaded_audio)