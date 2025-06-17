import streamlit as st

st.set_page_config(
    page_title = "Przykład 5"
)

st.write("Krótki przykład użycia kolumn, wierszy i suwaka.")
st.write("Wolisz psy, czy kotki?")

# container - umożliwia grupowanie elementów w aplikacji
row1 = st.container()

# row - umożliwia podział strony na wiersze
with row1:
    st.write("Wybierz swoje ulubione zwierzę:")
    # columns - umożliwia podział strony na kolumny
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Wolę pieski!"):
            st.write("Woof woof! ^0^")
    with col2:
        if st.button("Meow meow!"):
            st.write("Meow! ᓚᘏᗢ")
    with col3:
        if st.button("Lubię chomiki!"):
            st.write("Chomiki są super!")
row2 = st.container()
with row2:
    # slider - umożliwia wybór wartości z zakresu
    font_size = st.slider("Rozmiar czcionki:", 10, 100, 20)
row3 = st.container()
with row3:
    # wartość slidera jest używana do ustawienia rozmiaru czcionki w napisie
    st.write(f'<span style="font-size:{font_size}px">UwU</span>', unsafe_allow_html=True)