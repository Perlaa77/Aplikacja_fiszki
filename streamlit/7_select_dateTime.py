import streamlit as st
from datetime import time, date

st.set_page_config(
    page_title = "Przykład 7"
)

# Form - utworzenie formularza rezerwacji sali
with st.form("Formularz"):
    st.title("Formularz rezerwacji")

    # Selectbox - wybór typu sali
    room_type = st.selectbox(
        "Wybierz typ sali:",
        ["Sala konferencyjna", "Sala szkoleniowa", "Sala komputerowa"]
    )

    # Multiselect - wybór wyposażenia
    equipment = st.multiselect(
        "Wybierz wyposażenie:",
        ["Rzutnik", "Tablica suchościeralna", "Nagłośnienie", "Klimatyzacja", "Laptopy"]
    )

    # Date input - wybór daty
    reservation_date = st.date_input(
        "Wybierz datę rezerwacji:",
        min_value=date.today()
    )

    # Time input - wybór godziny rozpoczęcia
    start_time = st.time_input(
        "Godzina rozpoczęcia:",
        value=time(9, 0)
    )

    submit = st.form_submit_button("Zatwierdź rezerwację")
    # Wyświetlenie podsumowania
    if submit:
        st.subheader("Podsumowanie wyboru:")
        st.write(f"Typ sali: {room_type}")
        st.write(f"Wyposażenie: {', '.join(equipment) if equipment else 'Brak'}")
        st.write(f"Data: {reservation_date.strftime('%Y-%m-%d')}")
        st.write(f"Godzina rozpoczęcia: {start_time.strftime('%H:%M')}")
