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
    div.stButton > button,
    div.stForm button {
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
    st.session_state.active_page = "Start"
if "selected_profile_id" not in st.session_state:
    st.session_state.selected_profile_id = None

# Sprawdzenie profilu
profile_id = st.session_state.selected_profile_id

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
if st.session_state.active_page == "Start":
    
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

    # Informacja jeśli nie wybrano profilu
    if st.session_state.selected_profile_id is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    st.header("Konfiguracja sesji nauki")
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

    # Informacja jeśli nie wybrano profilu
    if st.session_state.selected_profile_id is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    # Przyciski dodawania zestawów i fiszek
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Dodaj nowy zestaw", key="dodaj_zestaw"):
            st.session_state.manage_set_id = None
            st.session_state.active_page = "Dodaj zestaw"
            st.rerun()
    with col2:
        if st.button("➕ Dodaj nową fiszkę", key="dodaj_fiszke"):
            st.session_state.manage_set_id = None
            st.session_state.edit_card_id = None
            st.session_state.active_page = "Dodaj fiszkę"
            st.rerun()

    # Zestawy danego profilu
    st.markdown("---")
    st.header("Twoje zestawy:")
    profile_id = st.session_state.selected_profile_id
    user_sets = zestawy_df[zestawy_df["id_profilu"] == profile_id]
    if not user_sets.empty:
        for _, row in user_sets.iterrows():
            if st.button(row["nazwa"], key=f"zestaw_{row['id']}"):
                st.session_state.manage_set_id = row["id"]
                st.session_state.active_page = "Fiszki w zestawie"
                st.rerun()
    else:
        st.write("Brak zestawów.")

    # Fiszki bez przypisanego zestawu
    st.markdown("---")
    unassigned = fiszki_df[
        (fiszki_df["id_profilu"] == profile_id) &
        (fiszki_df["id_zestawu"].isna())
    ]
    if not unassigned.empty:
        if st.button("Fiszki bez zestawu"):
            st.session_state.manage_set_id = None
            st.session_state.active_page = "Fiszki w zestawie"
            st.rerun()
    else:
        st.write("Brak fiszek bez zestawu.")

########################################################################################################################################
# Strona zarządzania fiszkami w konkretnym zestawie
elif st.session_state.active_page == "Fiszki w zestawie":

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
                st.session_state.active_page = "Dodaj fiszkę"
                st.rerun()

########################################################################################################################################
# Strona dodawania i edycji zestawów
elif st.session_state.active_page == "Dodaj zestaw":

    # Sprawdzenie trybu: nowy czy edycja
    is_edit_mode = False
    zestaw_do_edycji = None
    if st.session_state.get("manage_set_id") is not None:
        zestaw_do_edycji = zestawy_df[zestawy_df["id"] == st.session_state.manage_set_id]
        if not zestaw_do_edycji.empty:
            zestaw_do_edycji = zestaw_do_edycji.iloc[0]
            is_edit_mode = True

    st.header("Edytuj zestaw" if is_edit_mode else "Dodaj nowy zestaw")
    if st.button("← Powrót do zestawów"):
        st.session_state.active_page = "Fiszki"
        st.rerun()

    # Formularz dodawania/edytowania zestawu
    with st.form("zestaw_formularz"):
        nazwa = st.text_input("Nazwa zestawu", value=zestaw_do_edycji["nazwa"] if is_edit_mode else "")
        submitted = st.form_submit_button("Zapisz zestaw")

        if submitted:
            if nazwa.strip() == "":
                st.info("Nazwa zestawu nie może być pusta.")
            elif (zestawy_df["nazwa"] == nazwa).any() and (not is_edit_mode or nazwa != zestaw_do_edycji["nazwa"]):
                st.info("Zestaw o takiej nazwie już istnieje.")
            else:
                if is_edit_mode:
                    zestawy_df.loc[zestawy_df["id"] == zestaw_do_edycji["id"], "nazwa"] = nazwa
                    st.success("Zestaw został pomyślnie zaktualizowany.")
                else:
                    new_id = zestawy_df["id"].max() + 1 if not zestawy_df.empty else 1
                    new_row = pd.DataFrame([{
                        "id": new_id,
                        "nazwa": nazwa,
                        "id_profilu": profile_id
                    }])
                    zestawy_df = pd.concat([zestawy_df, new_row], ignore_index=True)
                    st.success("Nowy zestaw został pomyślnie dodany.")

                # Zapis zestawu
                zestawy_df.to_csv("data/zestawy.csv", sep=";", index=False)

                # Powrót do przeglądu zestawów
                st.session_state.active_page = "Fiszki"
                st.rerun()

########################################################################################################################################
# Strona dodawania i edycji fiszek
elif st.session_state.active_page == "Dodaj fiszkę":

    # Sprawdzenie trybu: nowy czy edycja
    is_edit_mode = False
    edytowana_fiszka = None
    if st.session_state.get("edit_card_id") is not None:
        edytowana_fiszka = fiszki_df[fiszki_df["id"] == st.session_state.edit_card_id]
        if not edytowana_fiszka.empty:
            edytowana_fiszka = edytowana_fiszka.iloc[0]
            is_edit_mode = True

    st.header("Edytuj fiszkę" if is_edit_mode else "Dodaj nową fiszkę")
    if st.button("← Powrót do zestawu"):
        st.session_state.active_page = "Fiszki w zestawie"
        st.session_state.edit_card_id = None
        st.rerun()

    # Wybór zestawu
    zestawy_uzytkownika = zestawy_df[zestawy_df["id_profilu"] == profile_id]
    opcje_zestawow = ["Brak zestawu"] + zestawy_uzytkownika["nazwa"].tolist()
    default_set_name = "Brak zestawu"
    if is_edit_mode and not pd.isna(edytowana_fiszka["id_zestawu"]):
        zestaw_row = zestawy_uzytkownika[zestawy_uzytkownika["id"] == edytowana_fiszka["id_zestawu"]]
        if not zestaw_row.empty:
            default_set_name = zestaw_row["nazwa"].values[0]
    elif st.session_state.get("manage_set_id") is not None:
        set_row = zestawy_uzytkownika[zestawy_uzytkownika["id"] == st.session_state["manage_set_id"]]
        if not set_row.empty:
            default_set_name = set_row["nazwa"].values[0]

    # Formularz dodawania/edytowania fiszki
    with st.form("add_flashcard_form"):
        przod = st.text_input("Przód (wymagane)", value=edytowana_fiszka["przod"] if is_edit_mode else "")
        podpowiedz = st.text_input("Podpowiedź (opcjonalna)", value=edytowana_fiszka["podpowiedz"] if is_edit_mode else "")
        tyl = st.text_input("Tył (wymagany)", value=edytowana_fiszka["tyl"] if is_edit_mode else "")
        rozwiniecie = st.text_area("Wyjaśnienie (opcjonalne)", value=edytowana_fiszka["rozwiniecie"] if is_edit_mode else "")
        wybrany_zestaw = st.selectbox("Zestaw", opcje_zestawow, index=opcje_zestawow.index(default_set_name))
        submitted = st.form_submit_button("Zapisz fiszkę")

        if submitted:
            if przod.strip() == "" or tyl.strip() == "":
                st.info("Uzupełnij wymagane pola: przód i tył.")
            else:
                if wybrany_zestaw == "Brak zestawu":
                    id_zestawu = np.nan
                else:
                    id_zestawu = zestawy_uzytkownika[zestawy_uzytkownika["nazwa"] == wybrany_zestaw]["id"].values[0]

                if is_edit_mode:
                    fiszki_df.loc[fiszki_df["id"] == edytowana_fiszka["id"], ["przod", "podpowiedz", "tyl", "rozwiniecie", "id_zestawu"]] = \
                        [przod, podpowiedz, tyl, rozwiniecie, id_zestawu]
                    st.success("Fiszka została zaktualizowana.")
                else:
                    new_id = fiszki_df["id"].max() + 1 if not fiszki_df.empty else 1
                    nowa_fiszka = pd.DataFrame([{
                        "id": new_id,
                        "przod": przod,
                        "podpowiedz": podpowiedz,
                        "tyl": tyl,
                        "rozwiniecie": rozwiniecie,
                        "id_profilu": profile_id,
                        "id_zestawu": id_zestawu
                    }])
                    fiszki_df = pd.concat([fiszki_df, nowa_fiszka], ignore_index=True)
                    st.success("Nowa fiszka została zapisana.")

                # Zapis fiszki
                fiszki_df.to_csv("data/fiszki.csv", sep=";", index=False)

                # Powrót do przeglądu zestawu
                st.session_state.active_page = "Fiszki w zestawie"
                st.session_state.edit_card_id = None
                st.rerun()

########################################################################################################################################
# Strona profilu
elif st.session_state.active_page == "Profil":
    st.header("Profil")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "selected_profile_id" not in st.session_state:
        st.session_state.selected_profile_id = None

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

########################################################################################################################################
# Strona rejestracji
elif st.session_state.active_page == "Rejestracja":
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