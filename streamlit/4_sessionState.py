import streamlit as st

st.set_page_config(
    page_title = "Przykład 4"
)

# Session_state sluzy do zapisywania danych
# miedzy ponownymy renderami aplikacji

# Inicjalizacja wartości w session_state
if "count" not in st.session_state:
    st.session_state.count = 0

# Funkcja zwiększająca licznik
def increment_counter():
    st.session_state.count += 1

st.title("Przykład użycia st.session_state")

# Przycisk do zwiększenia licznika
st.button("Kliknij mnie!", on_click=increment_counter)

# Wyświetlenie aktualnej wartości licznika
st.write(f"Licznik: {st.session_state.count}")
