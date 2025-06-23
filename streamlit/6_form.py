import streamlit as st

st.set_page_config(
    page_title = "Przykład 6"
)

st.write("Krótki przykład użycia przycisków, pól tekstowych, checkboxów, przycisków radiowych i pól numerycznych.")

# Form - umożliwia tworzenie formularzy, które można wysłać po kliknięciu przycisku; wysyła dane jednocześnie po zatwierdzeniu przyciskiem 
# (nie uruchamia przetwarzania przy każdej zmianie danych, tylko raz po kliknięciu przycisku)
with st.form("formularz"):

    st.write("Wypełnij poniższy formularz:")

    # Text input - możliwość wpisania tekstu
    name = st.text_input("Podaj swoje imię", "Twoje imię")

    # Number input - pole wyboru liczby, min value, max value - maksynmalna i minimalna wartość wyboru, value - wartość domyślna
    age = st.number_input("Podaj swój wiek", min_value=0, max_value=120, value=18)

    # Radio - przycisk wyboru tylko jednej opcji
    gender = st.radio("Wybierz płeć", ("Kobieta", "Mężczyzna", "Inna"))

    # Checkbox - pole wyboru, które można zaznaczyć lub odznaczyć
    newsletter = st.checkbox("Zapisz się do newslettera")

    # Submit button - przycisk do wysłania formularza (musi być w formularzu, aby działał; może być tylko jeden taki przycisk)
    submit = st.form_submit_button("Zatwierdź")

    if submit:
        st.write(f"Imię: {name}")
        st.write(f"Wiek: {age}")
        st.write(f"Płeć: {gender}")
        if newsletter:
            st.write("Zapisano do newslettera!")
        else:
            st.write("Nie zapisano do newslettera.")