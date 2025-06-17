import streamlit as st

st.set_page_config(
    page_title = "Przykład 6"
)

st.write("Krótki przykład użycia przycisków, pól tekstowych, checkboxów, przycisków radiowych i pól numerycznych.")

# Text input - możliwość wpisania tekstu
name = st.text_input("Podaj swoje imię", "Twoje imię")

# Przycisk - przycisk, który można kliknąć i wyświetlić komunikat
if st.button("Kliknij mnie"):
    st.write(f"Witaj, {name}!")

# Number input - pole wyboru liczby, min value, max value - maksynmalna i minimalna wartość wyboru, value - wartość domyślna
age = st.number_input("Podaj swój wiek", min_value=0, max_value=120, value=18)

# Radio - przycisk wyboru tylko jednej opcji
gender = st.radio("Wybierz płeć", ("Mężczyzna", "Kobieta", "Inna"))

# Checkbox - pole wyboru, które można zaznaczyć lub odznaczyć
newsletter = st.checkbox("Zapisz się do newslettera")

if st.button("Zatwierdź"):
    st.write(f"Imię: {name}")
    st.write(f"Wiek: {age}")
    st.write(f"Płeć: {gender}")
    if newsletter:
        st.write("Zapisano do newslettera!")
    else:
        st.write("Nie zapisano do newslettera.")