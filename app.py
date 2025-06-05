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
if "aktywna_strona" not in st.session_state:
    st.session_state.aktywna_strona = "Start"
if "id_aktywnego_profilu" not in st.session_state:
    st.session_state.id_aktywnego_profilu = None

st.markdown("---")

# Pasek nawigacyjny
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Start"):
        st.session_state.aktywna_strona = "Start"
with col2:
    if st.button("Ucz się"):
        st.session_state.aktywna_strona = "Ucz się"
with col3:
    if st.button("Fiszki"):
        st.session_state.aktywna_strona = "Fiszki"
with col4:
    if st.button("Profil"):
        st.session_state.aktywna_strona = "Profil"

st.markdown("---")

########################################################################################################################################
# Strona główna
if st.session_state.aktywna_strona == "Start":
    
    # Powitanie
    if st.session_state.id_aktywnego_profilu is not None:
        nick = profile_df.loc[profile_df["id"] == st.session_state.id_aktywnego_profilu, "nick"].values[0]
        st.header(f"👋 Cześć, {nick}!")
    else:
        st.header("👋 Cześć!")

    # Informacja jeśli nie wybrano profilu
    if st.session_state.id_aktywnego_profilu is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")

########################################################################################################################################
# Strona konfiguracji nauki
elif st.session_state.aktywna_strona == "Ucz się":

    # Informacja jeśli nie wybrano profilu
    if st.session_state.id_aktywnego_profilu is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    st.header("Konfiguracja sesji nauki")
    # Wybór trybu nauki
    tryb_nauki = st.radio("Wybierz tryb nauki:", ['Klasyczny', 'Test'])
    # Opcje dodatkowe
    czasomierz = st.checkbox("Pokaż licznik czasu")

    # Wybór tematów - na razie jako placeholder
    st.selectbox("Wybierz temat(y):", options=["(Wybór dostępny wkrótce)"], index=0, disabled=True)

    if st.button("Rozpocznij naukę"):
        st.session_state.aktywna_strona = "Sesja nauki"
        st.rerun()

########################################################################################################################################
# Strona nauki
elif st.session_state.aktywna_strona == "Sesja nauki":

    if st.button("← Powrót do konfiguracji"):
        st.session_state.aktywna_strona = "Ucz się"
        st.rerun()

########################################################################################################################################
# Strona zarządzania zestawami
elif st.session_state.aktywna_strona == "Fiszki":

    # Informacja jeśli nie wybrano profilu
    if st.session_state.id_aktywnego_profilu is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    # Przyciski dodawania zestawów i fiszek
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Dodaj nowy zestaw", key="dodaj_zestaw"):
            st.session_state.id_aktywnego_zestawu = None
            st.session_state.aktywna_strona = "Dodaj zestaw"
            st.rerun()
    with col2:
        if st.button("➕ Dodaj nową fiszkę", key="dodaj_fiszke"):
            st.session_state.id_aktywnego_zestawu = None
            st.session_state.id_aktywnej_fiszki = None
            st.session_state.aktywna_strona = "Dodaj fiszkę"
            st.rerun()

    # Zestawy danego profilu
    st.markdown("---")
    st.header("Twoje zestawy:")
    zestawy_profilu = zestawy_df[zestawy_df["id_profilu"] == st.session_state.id_aktywnego_profilu]
    if not zestawy_profilu.empty:
        for _, row in zestawy_profilu.iterrows():
            if st.button(row["nazwa"], key=f"zestaw_{row['id']}"):
                st.session_state.id_aktywnego_zestawu = row["id"]
                st.session_state.aktywna_strona = "Fiszki w zestawie"
                st.rerun()
    else:
        st.write("Brak zestawów.")

    # Fiszki bez przypisanego zestawu
    st.markdown("---")
    unassigned = fiszki_df[
        (fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu) &
        (fiszki_df["id_zestawu"].isna())
    ]
    if not unassigned.empty:
        if st.button("Fiszki bez zestawu"):
            st.session_state.id_aktywnego_zestawu = None
            st.session_state.aktywna_strona = "Fiszki w zestawie"
            st.rerun()
    else:
        st.write("Brak fiszek bez zestawu.")

########################################################################################################################################
# Strona zarządzania fiszkami w konkretnym zestawie
elif st.session_state.aktywna_strona == "Fiszki w zestawie":

    # Wyświetlanie fiszek w zestawie
    if st.session_state.id_aktywnego_zestawu is not None:
        zestaw = zestawy_df[zestawy_df["id"] == st.session_state.id_aktywnego_zestawu].iloc[0]
        st.header(f"Zestaw: {zestaw['nazwa']}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Dodaj fiszkę"):
                st.session_state.aktywna_strona = "Dodaj fiszkę"
                st.rerun()
        with col2:
            if st.button("✏️ Edytuj zestaw"):
                st.session_state.aktywna_strona = "Dodaj zestaw"
                st.rerun()
        fiszki = fiszki_df[
            (fiszki_df["id_zestawu"] == zestaw["id"]) &
            (fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu)
        ]
    # Wyświetlanie fiszek, które nie mają zestawu
    else:
        st.header("Fiszki bez zestawu")
        if st.button("➕ Dodaj fiszkę"):
            st.session_state.aktywna_strona = "Dodaj fiszkę"
            st.rerun()
        fiszki = fiszki_df[
            ((fiszki_df["id_zestawu"].isna()) | (fiszki_df["id_zestawu"] == "")) &
            (fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu)
        ]

    # Wyświetlanie w razie braku fiszek
    st.markdown("---")
    if fiszki.empty:
        st.write("Brak fiszek.")
    else:
        for _, row in fiszki.iterrows():
            if st.button(f"{row['przod']}", key=f"fiszka_{row['id']}"):
                st.session_state.id_aktywnej_fiszki = row["id"]
                st.session_state.aktywna_strona = "Dodaj fiszkę"
                st.rerun()

########################################################################################################################################
# Strona dodawania i edycji zestawów
elif st.session_state.aktywna_strona == "Dodaj zestaw":

    # Sprawdzenie trybu: nowy czy edycja
    tryb_edycji = False
    zestaw_do_edycji = None
    if st.session_state.get("id_aktywnego_zestawu") is not None:
        zestaw_do_edycji = zestawy_df[zestawy_df["id"] == st.session_state.id_aktywnego_zestawu]
        if not zestaw_do_edycji.empty:
            zestaw_do_edycji = zestaw_do_edycji.iloc[0]
            tryb_edycji = True

    st.header("Edytuj zestaw" if tryb_edycji else "Dodaj nowy zestaw")
    if st.button("← Powrót do zestawów"):
        st.session_state.aktywna_strona = "Fiszki"
        st.rerun()

    # Formularz dodawania/edytowania zestawu
    with st.form("add_set_form"):
        nazwa = st.text_input("Nazwa zestawu", value=zestaw_do_edycji["nazwa"] if tryb_edycji else "")
        col_zapisz, col_anuluj_usun = st.columns(2)
        with col_zapisz:
            submitted = st.form_submit_button("Zapisz zestaw")
        with col_anuluj_usun:
            cancelled = st.form_submit_button("Usuń zestaw" if tryb_edycji else "Anuluj")

        if submitted:
            if nazwa.strip() == "":
                st.info("Nazwa zestawu nie może być pusta.")
            elif (zestawy_df["nazwa"] == nazwa).any() and (not tryb_edycji or nazwa != zestaw_do_edycji["nazwa"]):
                st.info("Zestaw o takiej nazwie już istnieje.")
            else:
                if tryb_edycji:
                    zestawy_df.loc[zestawy_df["id"] == zestaw_do_edycji["id"], "nazwa"] = nazwa
                    st.success("Zestaw został pomyślnie zaktualizowany.")
                else:
                    new_id = zestawy_df["id"].max() + 1 if not zestawy_df.empty else 1
                    new_row = pd.DataFrame([{
                        "id": new_id,
                        "nazwa": nazwa,
                        "id_profilu": st.session_state.id_aktywnego_profilu
                    }])
                    zestawy_df = pd.concat([zestawy_df, new_row], ignore_index=True)
                    st.success("Nowy zestaw został pomyślnie dodany.")

                # Zapis zestawu
                zestawy_df.to_csv("data/zestawy.csv", sep=";", index=False)

                # Powrót do przeglądu zestawów
                st.session_state.aktywna_strona = "Fiszki"
                st.rerun()
        if cancelled:
            if tryb_edycji:
                zestawy_df = zestawy_df[zestawy_df["id"] != zestaw_do_edycji["id"]]
                zestawy_df.to_csv("data/zestawy.csv", sep=";", index=False)
                st.success("Zestaw został usunięty.")
            st.session_state.aktywna_strona = "Fiszki"
            st.rerun()

########################################################################################################################################
# Strona dodawania i edycji fiszek
elif st.session_state.aktywna_strona == "Dodaj fiszkę":

    # Sprawdzenie trybu: nowy czy edycja
    tryb_edycji = False
    edytowana_fiszka = None
    if st.session_state.get("id_aktywnej_fiszki") is not None:
        edytowana_fiszka = fiszki_df[fiszki_df["id"] == st.session_state.id_aktywnej_fiszki]
        if not edytowana_fiszka.empty:
            edytowana_fiszka = edytowana_fiszka.iloc[0]
            tryb_edycji = True

    st.header("Edytuj fiszkę" if tryb_edycji else "Dodaj nową fiszkę")
    if st.button("← Powrót do zestawu"):
        st.session_state.aktywna_strona = "Fiszki w zestawie"
        st.session_state.id_aktywnej_fiszki = None
        st.rerun()

    # Wybór zestawu
    zestawy_uzytkownika = zestawy_df[zestawy_df["id_profilu"] == st.session_state.id_aktywnego_profilu]
    opcje_zestawow = ["Brak zestawu"] + zestawy_uzytkownika["nazwa"].tolist()
    domyslna_nazwa_zestawu = "Brak zestawu"
    if tryb_edycji and not pd.isna(edytowana_fiszka["id_zestawu"]):
        row_zestaw = zestawy_uzytkownika[zestawy_uzytkownika["id"] == edytowana_fiszka["id_zestawu"]]
        if not row_zestaw.empty:
            domyslna_nazwa_zestawu = row_zestaw["nazwa"].values[0]
    elif st.session_state.get("id_aktywnego_zestawu") is not None:
        row_zestaw = zestawy_uzytkownika[zestawy_uzytkownika["id"] == st.session_state["id_aktywnego_zestawu"]]
        if not row_zestaw.empty:
            domyslna_nazwa_zestawu = row_zestaw["nazwa"].values[0]

    # Formularz dodawania/edytowania fiszki
    with st.form("add_flashcard_form"):
        przod = st.text_input("Przód (wymagane)", value=edytowana_fiszka["przod"] if tryb_edycji else "")
        podpowiedz = st.text_input("Podpowiedź (opcjonalna)", value=edytowana_fiszka["podpowiedz"] if tryb_edycji else "")
        tyl = st.text_input("Tył (wymagany)", value=edytowana_fiszka["tyl"] if tryb_edycji else "")
        rozwiniecie = st.text_area("Wyjaśnienie (opcjonalne)", value=edytowana_fiszka["rozwiniecie"] if tryb_edycji else "")
        wybrany_zestaw = st.selectbox("Zestaw", opcje_zestawow, index=opcje_zestawow.index(domyslna_nazwa_zestawu))
        col_zapisz, col_anuluj_usun = st.columns(2)
        with col_zapisz:
            submitted = st.form_submit_button("Zapisz fiszkę")
        with col_anuluj_usun:
            cancelled = st.form_submit_button("Usuń fiszkę" if tryb_edycji else "Anuluj")

        if submitted:
            if przod.strip() == "" or tyl.strip() == "":
                st.info("Uzupełnij wymagane pola: przód i tył.")
            else:
                if wybrany_zestaw == "Brak zestawu":
                    id_zestawu = np.nan
                else:
                    id_zestawu = zestawy_uzytkownika[zestawy_uzytkownika["nazwa"] == wybrany_zestaw]["id"].values[0]

                if tryb_edycji:
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
                        "id_profilu": st.session_state.id_aktywnego_profilu,
                        "id_zestawu": id_zestawu
                    }])
                    fiszki_df = pd.concat([fiszki_df, nowa_fiszka], ignore_index=True)
                    st.success("Nowa fiszka została zapisana.")

                # Zapis fiszki
                fiszki_df.to_csv("data/fiszki.csv", sep=";", index=False)

                # Powrót do przeglądu zestawu
                st.session_state.aktywna_strona = "Fiszki w zestawie"
                st.session_state.id_aktywnej_fiszki = None
                st.rerun()
        if cancelled:
            if tryb_edycji:
                fiszki_df = fiszki_df[fiszki_df["id"] != edytowana_fiszka["id"]]
                fiszki_df.to_csv("data/fiszki.csv", sep=";", index=False)
                st.success("Fiszka została usunięta.")
            st.session_state.aktywna_strona = "Fiszki w zestawie"
            st.session_state.id_aktywnej_fiszki = None
            st.rerun()

########################################################################################################################################
# Strona profilu
elif st.session_state.aktywna_strona == "Profil":
    st.header("Profil")

    if "zalogowany" not in st.session_state:
        st.session_state.zalogowany = False
    if "id_aktywnego_profilu" not in st.session_state:
        st.session_state.id_aktywnego_profilu = None

    if not st.session_state.zalogowany:
        st.subheader("🔐 Zaloguj się")

        login_nick = st.text_input("Login (nick)")
        login_haslo = st.text_input("Hasło", type="password")

        if st.button("Zaloguj"):
            profil = profile_df[profile_df["nick"] == login_nick]
            if not profil.empty:
                haslo_w_bazie = profil["haslo"].values[0]
                if haslo_w_bazie == login_haslo:
                    st.session_state.zalogowany = True
                    st.session_state.id_aktywnego_profilu = profil["id"].values[0]
                    st.success("Zalogowano pomyślnie.")
                    st.rerun()
                else:
                    st.error("Nieprawidłowe hasło.")
            else:
                st.error("Nie znaleziono użytkownika.")

        if st.button("Zarejestruj się"):
            st.session_state.aktywna_strona = "Rejestracja"
            st.rerun()

########################################################################################################################################
# Strona rejestracji
elif st.session_state.aktywna_strona == "Rejestracja":
    st.header("Rejestracja")
    with st.form("registration_form"):
        new_nick = st.text_input("Nazwa użytkownika")
        new_password = st.text_input("Hasło", type="password")
        potwierdz_haslo = st.text_input("Potwierdź hasło", type="password")
        submitted = st.form_submit_button("Zarejestruj")

        if submitted:
            # Walidacja
            if new_nick.strip() == "" or new_password.strip() == "":
                st.error("Nazwa użytkownika i hasło są wymagane.")
            elif new_nick in profile_df["nick"].values:
                st.error("Taki użytkownik już istnieje.")
            elif new_password != potwierdz_haslo:
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