"""
Fistaszki
Aplikacja do nauki z fiszkami.

Projekt z Uniwersalnych Metod Projektowania Aplikacji Na Urządzenia Mobilne i Wbudowane

[Któtki opis podsumowywujący]

Autorzy: [nasze imiona i nazwiska, uzupełnić gdy już kod będzie gotowy]
Wersja: 1.0
"""
########################################################################################################################################
# Podstawowa konfiguracja strony
import streamlit as st
st.set_page_config(
    page_title="Fistaszki",
    page_icon="🥜",
    layout="wide"
)

# Pozostałe importy
import pandas as pd
import numpy as np
import bcrypt as bc
import streamlit_cookies_manager as stcm
import time as ti

# Inicjalizacja ciasteczek
ciasteczka = stcm.EncryptedCookieManager(
    prefix="fistaszki",
    password="fis",
)

########################################################################################################################################
# Style strony
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

    /* Fiszka */       
    .fiszka-box {
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        padding: 30px;
        margin: 20px auto;
        max-width: 700px;
        font-size: 20px;
        color: black;
        text-align: center;
    }
    .fiszka-box h3 {
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

########################################################################################################################################
# Funkcje do haseł (hashowanie oraz porównanie wprowadzonego hasła z tym w bazie)
def hash_haslo(haslo: str) -> str:
    """
    Hashuje hasło i konwertuje je do formatu str.
    
    Args:
        haslo (str): Hasło w formie tekstowej
        
    Returns:
        str: Zakodowane hasło
        
    Note:
        Hasło jest konwertowane najpierw do formatu bajtów, po czym do str, aby umożliwić bezproblemowe przechowywanie go w pliku CSV.
    """
    haslo_shashowane = bc.hashpw(haslo.encode('utf-8'), bc.gensalt())
    return haslo_shashowane.decode('utf-8')
def sprawdz_haslo(podane_haslo: str, haslo_z_bazy: str) -> bool:
    """
    Sprawdza czy podane hasło zgadza się z hasłem przechowywanym w bazie.
    
    Args:
        podane_haslo (str): Hasło podane przez użytwkonika
        haslo_z_bazy (str): Zakodowane hasło odczytane z bazy
        
    Returns:
        bool: True, jeśli podane hasło zgadza się z hasłem w bazie.
        
    Note:
        Hasło podane przez użytkownika jest hashowane do formatu bajtów.
        Zakodowane hasło z bazy również jest przekonwertowywane do formatu bajtów przed porównaniem.
    """
    haslo_z_bazy_bajty = haslo_z_bazy.encode('utf-8')
    return bc.checkpw(podane_haslo.encode('utf-8'), haslo_z_bazy_bajty)

# Wczytanie danych z CSV
def zaladuj_dane_z_CSV(sciezka, kolumny):
    """
    Ładuje dane z pliku CSV z obsługą błędów.
    
    Args:
        sciezka (str): Ścieżka do pliku CSV
        kolumny (list): Lista nazw kolumn, które ma zawierać dana tablica danych
        
    Returns:
        pandas.DataFrame: Załadowane dane lub pusty DataFrame przy błędzie
        
    Note:
        Używa separatora średnika (;) do rozdzielania danych
    """
    try:
        return pd.read_csv(sciezka, sep=";")
    except:
        st.info("Wystąpił błąd przy ładowaniu danych z bazy")
        return pd.DataFrame(columns=kolumny)
    
profile_df = zaladuj_dane_z_CSV("data/profile.csv", ["id", "nick", "haslo"])
zestawy_df = zaladuj_dane_z_CSV("data/zestawy.csv", ["id", "nazwa", "opis", "id_profilu"])
fiszki_df = zaladuj_dane_z_CSV("data/fiszki.csv", ["id", "przod", "podpowiedz", "tyl", "rozwiniecie", "id_profilu", "id_zestawu"])

# Stan aplikacji - ustawienie aktywnej strony przy pierwszym uruchomieniu
if "aktywna_strona" not in st.session_state:
    st.session_state.aktywna_strona = "Start"

# Stan profilu - sprawdzenie ciasteczek i ustawienie zalogowanego profilu
if "id_aktywnego_profilu" not in st.session_state:
    if "id_aktywnego_profilu" in ciasteczka:
        try:
            st.session_state.id_aktywnego_profilu = int(ciasteczka["id_aktywnego_profilu"])
            st.session_state.zalogowany = True
        except:
            st.session_state.zalogowany = False
            st.session_state.id_aktywnego_profilu = None
    else:
        st.session_state.zalogowany = False
        st.session_state.id_aktywnego_profilu = None

st.markdown("---")

########################################################################################################################################
# Pasek nawigacyjny na górze stron
if st.session_state.aktywna_strona != "Sesja nauki" and st.session_state.aktywna_strona != "Podsumowanie sesji":
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
        if "ostatnia_sesja" in st.session_state:
            if st.button("🔁 Powtórz ostatnią sesję"):
                st.session_state.tryb_nauki = st.session_state.ostatnia_sesja["tryb"]
                st.session_state.czasomierz = st.session_state.ostatnia_sesja["czasomierz"]
                st.session_state.fiszki_do_nauki = st.session_state.ostatnia_sesja["fiszki"]
                st.session_state.aktywna_strona = "Sesja nauki"
                st.session_state.start_time = ti.time()
                st.rerun()

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

    # Wybór trybu nauki
    tryb_opis = {
        "Klasyczny": "Kliknij na fiszkę, by zobaczyć jej tył.", # przód, przycisk by zobaczyć podp, przycisk do obrotu (tył oraz wyjaśnienie), przyciski wstecz i dalej/"Zakończ sesję"
        "Trening": "Wpisz odpowiedź i sprawdź, czy jest poprawna.", # przód, przycisk by zobaczyć podp, pole na wpisanie własnej odpowiedzi, przycisk do obrotu/"Sprawdź odpowiedź" (tył oraz wyjaśnienie plus info czy odp była poprawna), przyciski wstecz i dalej/"Zakończ sesję"
        "Test": "Wpisz odpowiedzi dla wszystkich fiszek i sprawdź wynik w podsumowaniu." # przód, przycisk by zobaczyć podp, pole na wpisanie własnej odpowiedzi, przycisk dalej/"Zakończ sesję"
    }
    tryb_nauki = st.selectbox(
        "Wybierz tryb nauki:",
        options=list(tryb_opis.keys()),
        index=0
    )
    st.write(f"{tryb_opis[tryb_nauki]}")

    # Czasomierz
    czasomierz = st.checkbox("⏱️ Pokaż licznik czasu")

    st.markdown("---")

    # Wybór zestawów do nauki
    zestawy_uzytkownika = zestawy_df[zestawy_df["id_profilu"] == st.session_state.id_aktywnego_profilu]
    fiszki_uzytkownika = fiszki_df[fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu]

    wszystkie_opcje_zestawow = zestawy_uzytkownika["nazwa"].tolist()
    if not fiszki_uzytkownika[fiszki_uzytkownika["id_zestawu"] == 0].empty:
        wszystkie_opcje_zestawow.append("Bez zestawu")

    wybrane_zestawy = st.multiselect("Wybierz zestawy do nauki:", options=wszystkie_opcje_zestawow)

    # Wybór konkretnych fiszek do nauki
    fiszki_do_wyboru = pd.DataFrame()
    if wybrane_zestawy:
        fiszki_z_wybranych = pd.DataFrame()
        for nazwa in wybrane_zestawy:
            if nazwa == "Bez zestawu":
                temp = fiszki_uzytkownika[fiszki_uzytkownika["id_zestawu"] == 0]
            else:
                id_zestawu = zestawy_uzytkownika[zestawy_uzytkownika["nazwa"] == nazwa]["id"].values[0]
                temp = fiszki_uzytkownika[fiszki_uzytkownika["id_zestawu"] == id_zestawu]
            fiszki_z_wybranych = pd.concat([fiszki_z_wybranych, temp], ignore_index=True)
        if not fiszki_z_wybranych.empty:
            fiszki_z_wybranych["etykieta"] = fiszki_z_wybranych["przod"] + " ➝ " + fiszki_z_wybranych["tyl"]
            wybrane_fiszki = st.multiselect(
                "(Opcjonalnie) wybierz konkretne fiszki do nauki:",
                options=fiszki_z_wybranych["etykieta"].tolist()
            )
            fiszki_do_wyboru = fiszki_z_wybranych[fiszki_z_wybranych["etykieta"].isin(wybrane_fiszki)]
        else:
            st.info("Brak fiszek w wybranych zestawach.")
    else:
        st.info("Wybierz co najmniej jeden zestaw, aby zobaczyć fiszki.")

    st.markdown("---")

    # Rozpoczęcie nauki
    if st.button("Rozpocznij sesję"):
        if wybrane_zestawy and (not fiszki_z_wybranych.empty):
            st.session_state.tryb_nauki = tryb_nauki
            st.session_state.czasomierz = czasomierz
            if not fiszki_do_wyboru.empty:
                st.session_state.fiszki_do_nauki = fiszki_do_wyboru.to_dict(orient="records")
            else:
                st.session_state.fiszki_do_nauki = fiszki_z_wybranych.to_dict(orient="records")

            # Zapamiętanie ostatniej sesji
                st.session_state.ostatnia_sesja = {
                    "tryb": tryb_nauki,
                    "czasomierz": czasomierz,
                    "fiszki": st.session_state.fiszki_do_nauki
                }


            st.session_state.aktywna_strona = "Sesja nauki"
            st.session_state.start_time = ti.time()
            st.rerun()
        else:
            st.info("Musisz wybrać co najmniej jeden zestaw zawierający fiszki.")

########################################################################################################################################
# Strona nauki
elif st.session_state.aktywna_strona == "Sesja nauki":
    st.header(f"Tryb nauki: {st.session_state.tryb_nauki}")
    st.markdown("---")

    # Inicjalizacja stanu sesji
    if "indeks_fiszki" not in st.session_state:
        st.session_state.indeks_fiszki = 0
        st.session_state.odwrocona = False
        st.session_state.pokaz_podpowiedz = False
        st.session_state.odpowiedzi_uzytkownika = {}

    fiszki = st.session_state.fiszki_do_nauki
    indeks = st.session_state.indeks_fiszki
    fiszka = fiszki[indeks]

    # Czasomierz
    if st.session_state.czasomierz:
        czas = int(ti.time() - st.session_state.start_time)
        st.write(f"⏱️ Czas: {czas//60}:{czas%60:02d}")

    st.subheader(f"Fiszka {indeks+1} z {len(fiszki)}")

    # Wyświetlanie przodu fiszki
    st.markdown(f'<div class="fiszka-box"><h3>{fiszka["przod"]}</h3></div>', unsafe_allow_html=True)

    if st.session_state.pokaz_podpowiedz and fiszka["podpowiedz"]:
        st.info(f"💡 Podpowiedź: {fiszka['podpowiedz']}")

    if not st.session_state.pokaz_podpowiedz and fiszka["podpowiedz"]:
        if st.button("👁️ Pokaż podpowiedź"):
            st.session_state.pokaz_podpowiedz = True
            st.rerun()

    tryb = st.session_state.tryb_nauki

    if tryb == "Klasyczny":
        if st.session_state.odwrocona:
            st.markdown(f'<div class="fiszka-box"><h3>{fiszka["tyl"]}</h3></div>', unsafe_allow_html=True)
            if fiszka["rozwiniecie"]:
                st.markdown(f'<div class="fiszka-box" style="font-size:16px;"><i>{fiszka["rozwiniecie"]}</i></div>', unsafe_allow_html=True)

        if st.button("🔄 Odwróć fiszkę"):
            st.session_state.odwrocona = not st.session_state.odwrocona

    elif tryb == "Trening":
        odp = st.text_input("✏️ Twoja odpowiedź:", value=st.session_state.odpowiedzi_uzytkownika.get(indeks, ""))
        if st.button("✅ Sprawdź odpowiedź"):
            st.session_state.odpowiedzi_uzytkownika[indeks] = odp
            st.session_state.odwrocona = True
        if st.session_state.odwrocona:
            poprawna = fiszka["tyl"].strip().lower()
            uzytkowa = odp.strip().lower()
            if poprawna == uzytkowa:
                st.success("✅ Poprawna odpowiedź!")
            else:
                st.error(f"❌ Błędna. Poprawna to: **{fiszka['tyl']}**")
            if fiszka["rozwiniecie"]:
                  st.markdown(f'<div class="fiszka-box" style="font-size:16px;"><i>{fiszka["rozwiniecie"]}</i></div>', unsafe_allow_html=True)

    elif tryb == "Test":
        odp = st.text_input("✏️ Twoja odpowiedź:", value=st.session_state.odpowiedzi_uzytkownika.get(indeks, ""))
        st.session_state.odpowiedzi_uzytkownika[indeks] = odp

    st.markdown("---")

    # Nawigacja
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    with col1:
        if st.button("←", disabled=indeks == 0):
            st.session_state.indeks_fiszki -= 1
            st.session_state.odwrocona = False
            st.session_state.pokaz_podpowiedz = False
            st.rerun()
    with col5:
        if st.button("→", disabled=indeks == len(fiszki) - 1):
            st.session_state.indeks_fiszki += 1
            st.session_state.odwrocona = False
            st.session_state.pokaz_podpowiedz = False
            st.rerun()
    with col3:
        if st.button("❌ Zakończ sesję"):
            st.session_state.aktywna_strona = "Podsumowanie sesji"
            st.rerun()

########################################################################################################################################
# Strona podsumowania sesji nauki
elif st.session_state.aktywna_strona == "Podsumowanie sesji":
    st.header("Podsumowanie")

    czas = int(ti.time() - st.session_state.start_time)
    st.write(f"⏱️ Czas: {czas//60}:{czas%60:02d}")
    st.markdown("---")

    tryb = st.session_state.tryb_nauki
    if tryb in ["Test", "Trening"]:
        st.subheader("📊 Wyniki")

        fiszki = st.session_state.fiszki_do_nauki
        odpowiedzi = st.session_state.odpowiedzi_uzytkownika
        poprawne = 0

        for i, fiszka in enumerate(fiszki):
            user_ans = odpowiedzi.get(i, "").strip().lower()
            correct = fiszka["tyl"].strip().lower()
            if user_ans == correct:
                poprawne += 1
                st.markdown(f"✅ **{fiszka['przod']}** → {user_ans}")
            else:
                st.markdown(f"❌ **{fiszka['przod']}** → {user_ans or '_brak odpowiedzi_'} (poprawna: {fiszka['tyl']})")

        st.write(f"**Wynik końcowy:** {poprawne} / {len(fiszki)}")

    st.markdown("---")

    if st.button("🔁 Wróć do konfiguracji"):
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
        (fiszki_df["id_zestawu"] == 0)
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
            (fiszki_df["id_zestawu"] == 0) & (fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu)
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
                    id_zestawu = 0
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
# Strona profilu / logowania
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
        zapamietaj_mnie = st.checkbox("Zapamiętaj mnie")

        if st.button("Zaloguj"):
            profil = profile_df[profile_df["nick"] == login_nick]
            if not profil.empty:
                haslo_w_bazie = profil["haslo"].values[0]
                if sprawdz_haslo(login_haslo, haslo_w_bazie):
                    st.session_state.zalogowany = True
                    st.session_state.id_aktywnego_profilu = profil["id"].values[0]
                    st.success("Zalogowano pomyślnie.")

                    if zapamietaj_mnie:
                        ciasteczka["id_aktywnego_profilu"] = str(st.session_state.id_aktywnego_profilu)
                        ciasteczka.save()

                    st.rerun()
                else:
                    st.error("Nieprawidłowy profil lub hasło.")
            else:
                st.error("Nieprawidłowy profil lub hasło.")

        if st.button("Zarejestruj się"):
            st.session_state.aktywna_strona = "Rejestracja"
            st.rerun()

    elif st.session_state.zalogowany:
        if st.button("Wyloguj się"):
            st.session_state.zalogowany = False
            st.session_state.id_aktywnego_profilu = None
            if "id_aktywnego_profilu" in ciasteczka:
                ciasteczka["id_aktywnego_profilu"] = str(st.session_state.id_aktywnego_profilu)
                ciasteczka.save()

            st.success("Wylogowano pomyślnie.")
            st.rerun()

########################################################################################################################################
# Strona rejestracji
elif st.session_state.aktywna_strona == "Rejestracja":
    st.header("Rejestracja")
    with st.form("registration_form"):
        nowy_profil = st.text_input("Nazwa użytkownika")
        nowe_haslo = st.text_input("Hasło", type="password")
        potwierdz_haslo = st.text_input("Potwierdź hasło", type="password")
        submitted = st.form_submit_button("Zarejestruj")

        if submitted:
            # Walidacja
            if nowy_profil.strip() == "" or nowe_haslo.strip() == "":
                st.error("Nazwa profilu i hasło są wymagane.")
            elif nowy_profil in profile_df["nick"].values:
                st.error("Ta nazwa profilu jest już zajęta.")
            elif nowe_haslo != potwierdz_haslo:
                st.error("Hasła muszą być takie same.")
            else:
                # Dodaj nowy profil
                nowe_id = profile_df["id"].max() + 1 if not profile_df.empty else 1
                nowe_haslo_shashowane = hash_haslo(nowe_haslo)
                nowy_row = pd.DataFrame([{
                    "id": nowe_id,
                    "nick": nowy_profil,
                    "haslo": nowe_haslo_shashowane
                }])
                profile_df = pd.concat([profile_df, nowy_row], ignore_index=True)
                profile_df.to_csv("data/profile.csv", sep=";", index=False)

                st.success("Rejestracja zakończona pomyślnie. Możesz się teraz zalogować.")