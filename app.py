import streamlit as st
import pandas as pd
import numpy as np

########################################################################################################################################
# Podstawowa konfiguracja strony
st.set_page_config(
    page_title="Fistaszki",
    page_icon="",
    layout="wide"
)

########################################################################################################################################
# Style
st.markdown('<div class="gradient-text">Fistaszki</div>', unsafe_allow_html=True)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@350&family=EB+Garamond:ital@0;1&family=Lexend+Giga:wght@100..900&family=Raleway:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)
st.markdown("""
<style>
    /* Główna czcionka */
    html, body, .stApp {
        font-family: "EB Garamond", !important;
        font-weight: 700 !important;   
            background-color: #FAD1D6 !important;
    }
    
    /* Wycentrowanie tekstu i dzieci w głównym kontenerze */
        [data-testid="stAppViewContainer"] {
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            height: 100vh !important;
            text-align: center !important;
            text-color: black !important;
        }
            
        body, div, p, span, input, button, textarea {
        font-family: 'Lexend Giga', sans-serif !important;
        font-weight: 200 !important;
    }

        .gradient-text {
        font-family: 'Lexend Giga', sans-serif;
        font-size: 64px;
        font-weight: 350;
        text-align: center;
        background: linear-gradient(90deg, #FFCCE5 5%, #cc0066 80%, #cc0066 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0px 0 20px 0;
    }
    
    /* Standardowe nagłówki */
            
    h2, h3 {
        font-family: 'Lexend Giga' !important;
        font-weight: 100 !important;
        font-style: normal;
    }
            
    /* Ogólny styl wszystkich przycisków */
    div.stButton > button {
        background-color: #C34E88;
        color: white;
        font-family: 'Lexend Giga' !important;
        font-weight: 100 !important;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }

    /* Hover efekt */
    div.stButton > button:hover {
        background-color: #BA015E;
        transform: scale(1.05);
        color: white !important;
    }

    /* Styl aktywnego przycisku */
    div.stButton > button.active-button {
        background: linear-gradient(90deg, #8a5a44, #ffb347);
        font-weight: bold;
        color: white !important; 
    }

    /* Responsywny układ przycisków nawigacyjnych */
    @media (max-width: 768px) {
        /* Kontener na przyciski w układzie 2x2 */
        [data-testid="column"] {
            min-width: 50% !important;
            flex: 0 1 50% !important;
        }
        
        /* Styl przycisków na mobile */
        .stButton>button {
            width: 90% !important;
            margin: 5px auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)

########################################################################################################################################
# Konfiguracja i pobranie danych z bazy

# Wczytanie danych z CSV
profile_df = pd.read_csv("data/profile.csv", sep=";")
zestawy_df = pd.read_csv("data/zestawy.csv", sep=";")
fiszki_df = pd.read_csv("data/fiszki.csv", sep=";")

# Stan aplikacji (aktywna strona oraz profil)
if "active_page" not in st.session_state:
    st.session_state.active_page = "Strona główna"
if "selected_profile_id" not in st.session_state:
    st.session_state.selected_profile_id = None

# Pasek nawigacyjny
st.markdown("---")
pages = ['Start', 'Ucz się', 'Fiszki', 'Profil']
clicked = None

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    if st.button(pages[0]):
        st.session_state.active_page = pages[0]
with col2:
    if st.button(pages[1]):
        st.session_state.active_page = pages[1]
with col3:
    if st.button(pages[2]):
        st.session_state.active_page = pages[2]
with col4:
    if st.button(pages[3]):
        st.session_state.active_page = pages[3]

st.markdown("---")

########################################################################################################################################
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

########################################################################################################################################
# Strona konfiguracji nauki
elif st.session_state.active_page == "Ucz się":
    st.header('Ucz się!')

    # Informacja jeśli nie wybrano profilu
    if st.session_state.selected_profile_id is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    st.subheader("Konfiguracja sesji nauki")
    # Wybór trybu nauki
    study_mode = st.radio("Wybierz tryb nauki:", ['Klasyczny', 'Test'])
    # Opcje dodatkowe
    show_timer = st.checkbox("Pokaż licznik czasu")

    # Wybór tematów - na razie jako placeholder
    st.selectbox("Wybierz temat(y):", options=["(Wybór dostępny wkrótce)"], index=0, disabled=True)

    if st.button("Rozpocznij naukę"):
        st.session_state.active_page = "Sesja nauki"
        st.rerun()

########################################################################################################################################
# Strona nauki
elif st.session_state.active_page == "Sesja nauki":

    if st.button("← Powrót do konfiguracji"):
        st.session_state.active_page = "Ucz się"
        st.rerun()

########################################################################################################################################
# Strona zarządzania zestawami
elif st.session_state.active_page == "Fiszki":
    st.header("Fiszki")

    # Informacja jeśli nie wybrano profilu
    if st.session_state.selected_profile_id is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    # Przyciski dodawania zestawów i fiszek
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Dodaj nowy zestaw", key="dodaj_zestaw"):
            st.session_state.active_page = "Dodaj zestaw"
            st.rerun()
    with col2:
        if st.button("➕ Dodaj nową fiszkę", key="dodaj_fiszke"):
            st.session_state.manage_set_id = None
            st.session_state.active_page = "Dodaj fiszkę"
            st.rerun()

    # Zestawy danego profilu
    st.markdown("---")
    st.subheader("Twoje zestawy:")
    profile_id = st.session_state.selected_profile_id
    user_sets = zestawy_df[zestawy_df["id_profilu"] == profile_id]
    if not user_sets.empty:
        for _, row in user_sets.iterrows():
            if st.button(row["nazwa"], key=f"zestaw_{row['id']}"):
                st.session_state.manage_set_id = row["id"]
                st.session_state.active_page = "Fiszki"
                st.rerun()
    else:
        st.write("Brak zestawów.")

    # Fiszki bez przypisanego zestawu
    st.markdown("---")
    st.subheader("Fiszki bez zestawu:")
    unassigned = fiszki_df[
        (fiszki_df["id_profilu"] == profile_id) &
        (fiszki_df["id_zestawu"].isna())
    ]
    if not unassigned.empty:
        if st.button("Fiszki bez zestawu"):
            st.session_state.manage_set_id = None
            st.session_state.active_page = "Fiszki"
            st.rerun()
    else:
        st.write("Brak fiszek bez zestawu.")

########################################################################################################################################
# Strona zarządzania fiszkami w konkretnym zestawie
elif st.session_state.active_page == "Fiszki":

    # Przycisk powrotu
    if st.button("← Powrót do zestawów"):
        st.session_state.active_page = "Fiszki"
        st.rerun()

    # Wyświetlanie fiszek w zestawie
    if st.session_state.manage_set_id is not None:
        zestaw = zestawy_df[zestawy_df["id"] == st.session_state.manage_set_id].iloc[0]
        st.header(f"Zestaw: {zestaw['nazwa']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Dodaj fiszkę"):
                st.session_state.active_page = "Dodaj fiszkę"
                st.rerun()
        with col2:
            if st.button("✏️ Edytuj zestaw"):
                st.session_state.active_page = "Dodaj zestaw"
                st.rerun()
        fiszki = fiszki_df[
            (fiszki_df["id_zestawu"] == zestaw["id"]) &
            (fiszki_df["id_profilu"] == st.session_state.selected_profile_id)
        ]
    # Wyświetlanie fiszek, które nie mają zestawu
    else:
        st.header("Fiszki bez zestawu")
        if st.button("➕ Dodaj fiszkę"):
            st.session_state.active_page = "Dodaj fiszkę"
            st.rerun()
        fiszki = fiszki_df[
            ((fiszki_df["id_zestawu"].isna()) | (fiszki_df["id_zestawu"] == "")) &
            (fiszki_df["id_profilu"] == st.session_state.selected_profile_id)
        ]

    # Wyświetlanie w razie braku fiszek
    st.markdown("---")
    if fiszki.empty:
        st.write("Brak fiszek.")
    else:
        for _, row in fiszki.iterrows():
            if st.button(f"{row['przod']}", key=f"fiszka_{row['id']}"):
                st.session_state.edit_card_id = row["id"]
                st.session_state.active_page = "Edytuj fiszkę" # albo zrobić osobno Edytuj i Dodaj, albo jakoś połączyć
                st.rerun()

########################################################################################################################################
# Strona dodawania zestawów
elif st.session_state.active_page == "Dodaj zestaw":

    if st.button("← Powrót do zestawów"):
        st.session_state.active_page = "Zestawy"
        st.rerun()

########################################################################################################################################
# Strona dodawania fiszek
elif st.session_state.active_page == "Dodaj fiszkę":

    if st.button("← Powrót do fiszek"):
        st.session_state.active_page = "Fiszki"
        st.rerun()

########################################################################################################################################
# Strona profilu
elif st.session_state.active_page == "Profil":
    st.header("Profil")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "selected_profile_id" not in st.session_state:
        st.session_state.selected_profile_id = None

    profile_df = pd.read_csv("data/profile.csv", sep=";")

    if not st.session_state.logged_in:
        st.subheader("🔐 Zaloguj się")

        login_nick = st.text_input("Login (nick)")
        login_password = st.text_input("Hasło", type="password")

        if st.button("Zaloguj"):
            user = profile_df[profile_df["nick"] == login_nick]
            if not user.empty:
                stored_hash = user["haslo"].values[0]
                if stored_hash == login_password:
                    st.session_state.logged_in = True
                    st.session_state.selected_profile_id = user["id"].values[0]
                    st.success("Zalogowano pomyślnie.")
                    st.rerun()
                else:
                    st.error("Nieprawidłowe hasło.")
            else:
                st.error("Nie znaleziono użytkownika.")

        if st.button("Zarejestruj się"):
            st.session_state.active_page = "Rejestracja"
            st.rerun()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Strona rejestracji
if st.session_state.active_page == "Rejestracja":
    st.header("Rejestracja")
    with st.form("registration_form"):
        new_nick = st.text_input("Nazwa użytkownika")
        new_password = st.text_input("Hasło", type="password")
        confirm_password = st.text_input("Potwierdź hasło", type="password")
        submitted = st.form_submit_button("Zarejestruj")

        if submitted:
            # Walidacja
            if new_nick.strip() == "" or new_password.strip() == "":
                st.error("Nazwa użytkownika i hasło są wymagane.")
            elif new_nick in profile_df["nick"].values:
                st.error("Taki użytkownik już istnieje.")
            elif new_password != confirm_password:
                st.error("Hasła nie są zgodne.")
            else:
                # Dodaj nowego użytkownika
                new_id = profile_df["id"].max() + 1 if not profile_df.empty else 1
                new_row = pd.DataFrame([{
                    "id": new_id,
                    "nick": new_nick,
                    "haslo": new_password
                }])
                profile_df = pd.concat([profile_df, new_row], ignore_index=True)
                profile_df.to_csv("data/profile.csv", sep=";", index=False)

                st.success("Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.")