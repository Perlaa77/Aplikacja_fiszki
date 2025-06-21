import streamlit as st

# pip install streamlit-option-menu - konieczne, by działał navigation bar, sidebar, container
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title = "Przykład 2"
)

st.write("Przykład użycia sidebar, expander, container w Streamlit.")

#SIdebar - pasek boczny, którym można nawigować po aplikacji
with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Wybór motywu", "Container", "Expander"],
        icons = ["house", "info-circle", "envelope"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "vertical"
    )

if selected == "Wybór motywu":
    st.write("Tu możesz wybrać motyw aplikacji.")
    # Expander - rozwijane menu, które można użyć do ukrycia lub pokazania dodatkowych informacji
    with st.expander("Ustawienia motywu"):
        theme = st.selectbox("Wybierz motyw", ["Ciemny", "Jasny"])
        # theme - zmienna przechowująca wybrany motyw
        if theme == "Jasny":
            # markdown - modyfiukuje wygląd aplikacji, można użyć do zmiany kolorów, czcionek itp.
            st.markdown("""
            <style>
            .stApp{background-color: white; color: black;}
            .css-18e3th9 { background-color: #1E1E1E; }
            .st-bb { background-color: #1E1E1E; }
            .st-at { background-color: #2E2E2E; }          
            </style>
            """, unsafe_allow_html=True)
            st.write("Wybrano motyw jasny.")
        else:
            st.markdown("""
            <style>
             .stApp{background-color: black; color: white;}           
            </style>
            """, unsafe_allow_html=True)
            st.write("Wybrano motyw ciemny.")   
if selected == "Container":
    st.title("Container w Streamlit")
    # Container - kontener, który pozwala na grupowanie elementów w aplikacji
    with st.container(border = True):
        st.write("To jest przykładowa aplikacja Streamlit, a konkretniej przykład użycia sidebar, expander i container.")
        st.write("To jest strona o nas.")

if selected == "Expander":
    st.write("Tu znajduje się przykładowy expander.")
    with st.expander("Formularz kontaktowy"):
        name = st.text_input("Imię i nazwisko")
        email = st.text_input("Email")
        message = st.text_area("Wiadomość")
        if st.button("Wyślij"):
            st.success(f"Dziękujemy za wiadomość, {name}!")