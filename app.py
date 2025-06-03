import streamlit as st
import pandas as pd
import numpy as np

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Podstawowa konfiguracja strony
st.set_page_config(
    page_title="Fistaszki",
    page_icon="",
    layout="wide"
)
st.title('Fistaszki')

# Wczytanie danych z CSV
profile_df = pd.read_csv("data/profile.csv", sep=";")
zestawy_df = pd.read_csv("data/zestawy.csv", sep=";")
fiszki_df = pd.read_csv("data/fiszki.csv", sep=";")

# Stan aplikacji (aktywna strona oraz profil)
if "active_page" not in st.session_state:
    st.session_state.active_page = "Strona główna"
if "selected_profile_id" not in st.session_state:
    st.session_state.selected_profile_id = None

# Pasek nawigacyjny (dla wszystkich stron poza "Sesja nauki")
if st.session_state.active_page != "Sesja nauki":
    page = st.sidebar.radio('', ['Strona główna','Ucz się','Zestawy i fiszki','Profil'])
    st.session_state.active_page = page

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strona główna
if st.session_state.active_page == "Strona główna":
    
    # Powitanie
    if st.session_state.selected_profile_id is not None:
        nick = profile_df.loc[profile_df["id"] == st.session_state.selected_profile_id, "nick"].values[0]
        st.header(f"👋 Cześć, {nick}!")
    else:
        st.header("👋 Cześć!")

    # Informacja jeśli nie wybrano profilu
    if st.session_state.selected_profile_id is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strona konfiguracji nauki
elif st.session_state.active_page == "Ucz się":
    st.header('Ucz się!')
    st.subheader("Konfiguracja sesji nauki")

    # Wybór trybu nauki
    study_mode = st.radio("Wybierz tryb nauki:", ['Klasyczny', 'Test'])

    # Opcje dodatkowe
    show_timer = st.checkbox("Pokaż licznik czasu")

    # Wybór tematów - na razie jako placeholder
    st.selectbox("Wybierz temat(y):", options=["(Wybór dostępny wkrótce)"], index=0, disabled=True)

    if st.button("Rozpocznij naukę"):
        st.session_state.active_page = "Sesja nauki"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strona nauki
elif st.session_state.active_page == "Sesja nauki":

    if st.button("← Powrót do konfiguracji"):
        st.session_state.active_page = "Ucz się"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strona zarządzania zestawami i fiszkami
elif st.session_state.active_page == "Zestawy i fiszki":
    st.subheader("elo")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strona profilu
elif st.session_state.active_page == "Profil":
    st.header("Profil")

    # Zalogowany jako
    if st.session_state.selected_profile_id is not None:
        nick = profile_df.loc[profile_df["id"] == st.session_state.selected_profile_id, "nick"].values[0]
    else:
        nick = "Gość"
    st.write(f"**Zalogowany jako:** {nick}")

    # Wybór profilu
    options = ["Gość"] + profile_df["nick"].tolist() + ["Dodaj nowy"]
    if "profile_choice" not in st.session_state:
        st.session_state.profile_choice = nick
    choice = st.radio("Wybierz profil:", options, index=options.index(st.session_state.profile_choice))

    # Przełączanie profilu
    if choice != st.session_state.profile_choice:
        st.session_state.profile_choice = choice
        if choice == "Gość":
            st.session_state.selected_profile_id = None
            st.rerun()
        elif choice != "Dodaj nowy":
            profile_id = profile_df.loc[profile_df["nick"] == choice, "id"].values[0]
            st.session_state.selected_profile_id = profile_id
            st.rerun()

    # Dodawanie nowego profilu
    if choice == "Dodaj nowy":
        new_nick = st.text_input("Podaj nazwę nowego profilu:")
        if st.button("Zatwierdź nowy profil"):
            if new_nick.strip() == "":
                st.error("Nazwa profilu nie może być pusta!")
            elif new_nick in profile_df["nick"].values:
                st.error("Profil o takiej nazwie już istnieje!")
            else:
                new_id = profile_df["id"].max() + 1 if not profile_df.empty else 1
                new_row = pd.DataFrame([{"id": new_id, "nick": new_nick}])
                profile_df = pd.concat([profile_df, new_row], ignore_index=True)
                profile_df.to_csv("data/profile.csv", sep=";", index=False)

                st.session_state.selected_profile_id = new_id
                st.session_state.profile_choice = new_nick
                st.success(f"Profil '{new_nick}' został dodany i wybrany.")
                st.rerun()
