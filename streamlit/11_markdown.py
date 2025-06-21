import streamlit as st

# Tytuł aplikacji
st.title("Przykład JavaScript w Streamlit")

# Przykład wstrzyknięcia JavaScriptu przez st.markdown
# Parametr unsafe_allow_html=True pozwala na użycie tagów <script> i innych elementów HTML
st.markdown("""
    <h3>Dynamiczny czas z JavaScript</h3>
    <p>Ten czas został wygenerowany za pomocą JavaScript:</p>
    <p id="time"></p>

    <script>
    // Prosty skrypt, który wyświetla bieżący czas i aktualizuje go co sekundę
    function updateTime() {
        var now = new Date();
        document.getElementById("time").innerText = now.toLocaleTimeString();
    }
    setInterval(updateTime, 1000);
    updateTime(); // wywołanie początkowe
    </script>
""", unsafe_allow_html=True)

# Dalsze komponenty Streamlit działają jak zwykle
st.write("Pozostałe komponenty Streamlit nadal działają poprawnie.")

# Przycisk do pokazania interakcji z Pythonem
if st.button("Kliknij mnie"):
    st.success("Przycisk został kliknięty — to działa po stronie Pythona.")
