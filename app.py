import streamlit as st
import pandas as pd
import numpy as np

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Podstawowa konfiguracja
st.set_page_config(
    page_title="Fistaszki",
    page_icon="",
    layout="wide"
)
st.title('Fistaszki')

# Pasek nawigacyjny
st.sidebar.title('')
page = st.sidebar.radio('', ['Witaj','Ucz się','Edytuj fiszki','Profil'])

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Strona główna
if page == 'Witaj':
    st.header('Fistaszki')
    st.subheader("Twoja aplikacja do nauki z fiszek")

    st.write("""
    Witaj w **Fistaszkach** – aplikacji wspierającej efektywną naukę z wykorzystaniem fiszek!
    Korzystaj z różnych trybów nauki, śledź swoje postępy i zarządzaj swoimi zestawami tematycznymi.
    """)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Strona nauki
if page == 'Ucz się':
    st.header('Ucz się!')
    st.subheader("Konfiguracja sesji nauki")

    # Wybór trybu nauki
    study_mode = st.radio("Wybierz tryb nauki:", ['Klasyczny', 'Test'])

    # Opcje dodatkowe
    show_timer = st.checkbox("Pokaż licznik czasu")

    # Wybór tematów - na razie jako placeholder
    st.selectbox("Wybierz temat(y):", options=["(Wybór dostępny wkrótce)"], index=0, disabled=True)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Strona edycji fiszek
if page == 'Edytuj fiszki':
    st.subheader("elo")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Strona profilowa
if page == 'Profil':
        st.subheader("elo")