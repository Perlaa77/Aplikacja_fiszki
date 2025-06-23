import streamlit as st

# Tytuł aplikacji
st.title("Użycie Markdown w Streamlit")

# Użycie Markdown do wstawienia sformatowanej zawartości HTML
# UWAGA: nie używamy <script>, tylko czysty HTML + CSS (inline)
st.markdown("""
<div style="padding: 1em; border-radius: 10px; background-color: #f0f8ff; border: 1px solid #add8e6;">
    <h3 style="color: #005f73;">Informacja</h3>
    <p style="font-size: 16px;">
        To jest <b>przykład użycia markdown z HTML</b> w Streamlit.
        Możemy stylować tekst, używać emoji i formatować tło.
    </p>
</div>
""", unsafe_allow_html=True)

# Zwykłe użycie Markdown bez HTML
st.markdown("### Lista zadań")
st.markdown("""
- Punkt pierwszy
- Punkt drugi
- Punkt trzeci
""")

# Standardowy komponent Streamlit
if st.checkbox("Pokaż więcej"):
    st.info("Tutaj znajduje się dodatkowa informacja.")
