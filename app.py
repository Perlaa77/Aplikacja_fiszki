"""
Fistaszki
Aplikacja do nauki z fiszkami.

Projekt z Uniwersalnych Metod Projektowania Aplikacji Na Urządzenia Mobilne i Wbudowane

[Któtki opis podsumowujący]

Autorzy: Hryciuk Aleksandra, Morawiec Victoria, Morchat Filip
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
import os
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
# Style strony i gradientowa nazwa
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
        font-size: 50px;
        font-weight: 350;
        text-align: center;
        background: #cc0066;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0px 0 20px 0;
    }

            
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

    /* Układ przycisków nawigacyjnych */
    @media (max-width: 768px) {
        /* Kontener na przyciski w układzie 2x2 */
        [data-testid="column"] {
            min-width: 50% !important;
            flex: 0 1 50% !important;
        }
        
        /* Styl przycisków*/
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
        font-size: 16px;
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
zestawy_df = zaladuj_dane_z_CSV("data/zestawy.csv", ["id", "nazwa", "opis", "id_profilu", "publiczny"])
fiszki_df = zaladuj_dane_z_CSV("data/fiszki.csv", ["id", "przod", "podpowiedz", "tyl", "rozwiniecie", "id_profilu", "id_zestawu"])
statystyki_df = zaladuj_dane_z_CSV("data/statystyki.csv", ["id_profilu", "data", "czas", "typ", "wynik", "liczba_fiszek"])

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
    
    # Jeśli zalogowany
    if st.session_state.id_aktywnego_profilu is not None:
        #Powitanie
        nick = profile_df.loc[profile_df["id"] == st.session_state.id_aktywnego_profilu, "nick"].values[0]
        st.header(f"👋 Cześć, {nick}!")

        # Powtórzenie ostatniej sesji
        if "ostatnia_sesja" in st.session_state:
            if st.button("Powtórz ostatnią sesję"):
                st.session_state.tryb_nauki = st.session_state.ostatnia_sesja["tryb"]
                st.session_state.czasomierz = st.session_state.ostatnia_sesja["czasomierz"]
                st.session_state.fiszki_do_nauki = st.session_state.ostatnia_sesja["fiszki"]
                st.session_state.aktywna_strona = "Sesja nauki"
                st.session_state.start_time = ti.time()
                st.rerun()

        # Wyszukiwanie fiszek
        st.subheader("Wyszukaj zestawy fiszek")
        fraza = st.text_input("Wpisz słowo kluczowe", placeholder="np. język angielski")
        if fraza:
            dopasowane_zestawy = zestawy_df[
                (zestawy_df["publiczny"] == True) & (
                zestawy_df["nazwa"].str.contains(fraza, case=False, na=False) |
                zestawy_df["opis"].str.contains(fraza, case=False, na=False)
                )
            ]
            if dopasowane_zestawy.empty:
                st.info("Brak zestawów spełniających kryteria.")
            else:
                for _, zestaw in dopasowane_zestawy.iterrows():
                    autor = "Nieznany"
                    try:
                        profile_match = profile_df.loc[profile_df["id"] == zestaw["id_profilu"], "nick"]
                        if not profile_match.empty:
                            autor = profile_match.values[0]
                    except:
                        pass

                    st.markdown(f"""
                    #### {zestaw['nazwa']}
                    **Opis:** {zestaw['opis']}  
                    **Autor:** {autor}
                    """)
                    
                    liczba_fiszek = fiszki_df[fiszki_df["id_zestawu"] == zestaw["id"]].shape[0]
                    st.write(f"Liczba fiszek w zestawie: {liczba_fiszek}")

                    if st.button(f"Ucz się z tego zestawu", key=f"start_{zestaw['id']}"):
                        st.session_state.aktywna_strona = "Ucz się"
                        st.session_state.wybrany_zestaw_do_nauki = {
                            'id': zestaw['id'],
                            'nazwa': zestaw['nazwa'],
                            'id_profilu': zestaw['id_profilu']
                        }
                        st.rerun()

    # Jeśli niezalogowany
    else:
        st.header("👋 Cześć!")
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
    
########################################################################################################################################
# Strona konfiguracji nauki
elif st.session_state.aktywna_strona == "Ucz się":

    # Informacja jeśli nie wybrano profilu
    if st.session_state.id_aktywnego_profilu is None:
        st.info("Aby korzystać z pełnej funkcjonalności aplikacji, przejdź do zakładki **Profil** i wybierz lub utwórz profil.")
        st.stop()

    # Wybór trybu nauki
    tryby = {
        "Klasyczny": "Kliknij na fiszkę, by zobaczyć jej tył.",
        "Trening": "Wpisz odpowiedź i sprawdź, czy jest poprawna.",
        "Test": "Wpisz odpowiedzi dla wszystkich fiszek i sprawdź wynik w podsumowaniu."
    }
    tryb_nauki = st.selectbox(
        "Wybierz tryb nauki:",
        options=list(tryby.keys()),
        index=0
    )
    st.write(f"{tryby[tryb_nauki]}")

    # Czasomierz
    czasomierz = st.checkbox("⏱️ Pokaż licznik czasu")

    st.markdown("---")

    # Wybór zestawów do nauki
    zestawy_uzytkownika = zestawy_df[    (zestawy_df["id_profilu"] == st.session_state.id_aktywnego_profilu) | (zestawy_df["publiczny"] == True)]
    fiszki_uzytkownika = fiszki_df[fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu]
    wszystkie_opcje_zestawow = zestawy_uzytkownika["nazwa"].tolist()

    default_wybrane_zestawy = []
    if 'wybrany_zestaw_do_nauki' in st.session_state:
        wybrany = st.session_state.wybrany_zestaw_do_nauki
        if isinstance(wybrany, dict):
            if wybrany['nazwa'] not in wszystkie_opcje_zestawow:
                wszystkie_opcje_zestawow.append(wybrany['nazwa'])
            default_wybrane_zestawy = [wybrany['nazwa']]
        elif isinstance(wybrany, list):
            for z in wybrany:
                if isinstance(z, dict):
                    if z['nazwa'] not in wszystkie_opcje_zestawow:
                        wszystkie_opcje_zestawow.append(z['nazwa'])
                    default_wybrane_zestawy.append(z['nazwa'])
                elif isinstance(z, str):  
                    if z not in wszystkie_opcje_zestawow:
                        wszystkie_opcje_zestawow.append(z)
                    default_wybrane_zestawy.append(z)

    # Wyświetlenie Multiselect
    wybrane_zestawy = st.multiselect(
        "Wybierz zestawy do nauki:",
        options=wszystkie_opcje_zestawow,
        default=default_wybrane_zestawy
    )
    zestawy_dict_list = []
    for nazwa in wybrane_zestawy:
        zestaw = zestawy_df[zestawy_df["nazwa"] == nazwa]
        if not zestaw.empty:
            rekord = zestaw.iloc[0]
            zestawy_dict_list.append({
                "id": rekord["id"],
                "id_profilu": rekord["id_profilu"],
                "nazwa": rekord["nazwa"]
            })

    # zapisz jako listę dictów
    st.session_state.wybrany_zestaw_do_nauki = zestawy_dict_list

    # Wybór konkretnych fiszek do nauki
    fiszki_do_wyboru = pd.DataFrame()
    if wybrane_zestawy:
        fiszki_z_wybranych = pd.DataFrame()
        
        for nazwa in wybrane_zestawy:
            # Fiszki bez zestawu
            if nazwa == "Bez zestawu":
                temp = fiszki_uzytkownika[fiszki_uzytkownika["id_zestawu"] == 0]
            # Fiszki w zestawach
            else:
                id_zestawu = None
                user_zestaw = zestawy_uzytkownika[zestawy_uzytkownika["nazwa"] == nazwa]
                if not user_zestaw.empty:
                    id_zestawu = user_zestaw["id"].values[0]
                    temp = fiszki_uzytkownika[fiszki_uzytkownika["id_zestawu"] == id_zestawu]
                else:
                    global_zestaw = zestawy_df[zestawy_df["nazwa"] == nazwa]
                    if not global_zestaw.empty:
                        id_zestawu = global_zestaw["id"].values[0]
                        temp = fiszki_df[fiszki_df["id_zestawu"] == id_zestawu]
                    else:
                        continue
            fiszki_z_wybranych = pd.concat([fiszki_z_wybranych, temp], ignore_index=True)
        
        if not fiszki_z_wybranych.empty:
            fiszki_z_wybranych["etykieta"] = fiszki_z_wybranych["przod"] + " ➝ " + fiszki_z_wybranych["tyl"]
            wybrane_fiszki = st.multiselect(
                "(Opcjonalnie) wybierz konkretne fiszki do nauki:",
                options=fiszki_z_wybranych["etykieta"].tolist()
            )
            fiszki_do_wyboru = fiszki_z_wybranych[fiszki_z_wybranych["etykieta"].isin(wybrane_fiszki)]
        else:
            st.info("Brak fiszek w wybranych zestawach. Sprawdź czy:")
            st.write("- Zestaw nie jest pusty")
            st.write("- Masz dostęp do fiszek w tym zestawie")
            st.write("- Fiszki są przypisane do właściwego zestawu")
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

            for key in ["indeks_fiszki", "odwrocona", "pokaz_podpowiedz", "odpowiedzi_uzytkownika"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.aktywna_strona = "Sesja nauki"
            st.session_state.start_time = ti.time()
            st.rerun()
        else:
            st.info("Musisz wybrać co najmniej jeden zestaw zawierający fiszki.")

########################################################################################################################################
# Strona nauki
elif st.session_state.aktywna_strona == "Sesja nauki":
    st.header(f"Tryb nauki: {st.session_state.tryb_nauki}")
    if st.session_state.fiszki_do_nauki:
        id_zestawu = st.session_state.fiszki_do_nauki[0]["id_zestawu"]
        if id_zestawu != 0:
            nazwa_zestawu = zestawy_df[zestawy_df["id"] == id_zestawu]["nazwa"].values[0]
            st.subheader(f"Zestaw: {nazwa_zestawu}")
        st.markdown("---")

    # Inicjalizacja stanu sesji
    if "indeks_fiszki" not in st.session_state:
        st.session_state.indeks_fiszki = 0
        st.session_state.odwrocona = False
        st.session_state.pokaz_podpowiedz = False
        st.session_state.odpowiedzi_uzytkownika = {}

    fiszka = st.session_state.fiszki_do_nauki[st.session_state.indeks_fiszki]

    # Czasomierz
    if st.session_state.czasomierz:
        czas = int(ti.time() - st.session_state.start_time)
        st.write(f"⏱️ Czas: {czas//60}:{czas%60:02d}")

    st.subheader(f"Fiszka {st.session_state.indeks_fiszki+1} z {len(st.session_state.fiszki_do_nauki)}")

    zawartosc_fiszki = f"<h3>{fiszka['przod']}</h3>"
    if st.session_state.odwrocona and st.session_state.tryb_nauki != "Test":
        zawartosc_fiszki = f"<h3>{fiszka['tyl']}</h3>"
        if fiszka["rozwiniecie"]:
            zawartosc_fiszki += f"<p style='font-size:14px;'><i>{fiszka['rozwiniecie']}</i></p>"
    st.markdown(f'<div class="fiszka-box">{zawartosc_fiszki}</div>', unsafe_allow_html=True)

    if not st.session_state.odwrocona and fiszka["podpowiedz"]:
        if st.session_state.pokaz_podpowiedz:
            st.info(f"Podpowiedź: {fiszka['podpowiedz']}")
        else:
            if st.button("Pokaż podpowiedź"):
                st.session_state.pokaz_podpowiedz = True
                st.rerun()

    # Tryby
    if st.session_state.tryb_nauki == "Klasyczny":
        if st.button("Odwróć fiszkę"):
            st.session_state.odwrocona = not st.session_state.odwrocona
            st.rerun()

    elif st.session_state.tryb_nauki == "Trening":
        odp = st.text_input("✏️ Twoja odpowiedź:", key=f"odp_{st.session_state.indeks_fiszki}", value=st.session_state.odpowiedzi_uzytkownika.get(st.session_state.indeks_fiszki, ""))
        if odp.strip() != "":
            st.session_state.odpowiedzi_uzytkownika[st.session_state.indeks_fiszki] = odp
        if st.button("Sprawdź odpowiedź"):
            st.session_state.odpowiedzi_uzytkownika[st.session_state.indeks_fiszki] = odp
            st.session_state.odwrocona = True
            st.rerun()
        if st.session_state.odwrocona:
            poprawna = fiszka["tyl"].strip().lower()
            uzytkowa = odp.strip().lower()
            if poprawna == uzytkowa:
                st.success("✅ Poprawna odpowiedź!")
            else:
                st.error(f"❌ Błędna. Poprawna to: **{fiszka['tyl']}**")

    elif st.session_state.tryb_nauki == "Test":
        odp = st.text_input("Twoja odpowiedź:", key=f"odp_{st.session_state.indeks_fiszki}", value=st.session_state.odpowiedzi_uzytkownika.get(st.session_state.indeks_fiszki, ""))
        if odp.strip() != "":
            st.session_state.odpowiedzi_uzytkownika[st.session_state.indeks_fiszki] = odp

    # Nawigacja
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("←", disabled=st.session_state.indeks_fiszki == 0):
            st.session_state.indeks_fiszki -= 1
            st.session_state.odwrocona = False
            st.session_state.pokaz_podpowiedz = False
            st.rerun()
    with col2:
        if st.button("❌ Zakończ sesję"):
            st.session_state.aktywna_strona = "Podsumowanie sesji"
            st.rerun()
    with col3:
        if st.button("→", disabled=st.session_state.indeks_fiszki == len(st.session_state.fiszki_do_nauki) - 1):
            st.session_state.indeks_fiszki += 1
            st.session_state.odwrocona = False
            st.session_state.pokaz_podpowiedz = False
            st.rerun()

########################################################################################################################################
# Strona podsumowania sesji nauki
elif st.session_state.aktywna_strona == "Podsumowanie sesji":
    st.header("Podsumowanie")

    czas = int(ti.time() - st.session_state.start_time)
    st.write(f"🕑 Czas: {czas//60}:{czas%60:02d}")

    tryb = st.session_state.tryb_nauki
    if tryb in ["Test", "Trening"]:
        st.subheader("Wyniki")

        odpowiedzi = st.session_state.odpowiedzi_uzytkownika
        poprawne = 0

        for i, fiszka in enumerate(st.session_state.fiszki_do_nauki):
            user_ans = odpowiedzi.get(i, "").strip().lower()
            correct = fiszka["tyl"].strip().lower()
            if user_ans == correct:
                poprawne += 1
                st.markdown(f"✅ **{fiszka['przod']}** → {user_ans}")
            else:
                st.markdown(f"❌ **{fiszka['przod']}** → {user_ans or '_brak odpowiedzi_'} (poprawna: {fiszka['tyl']})")

        st.write(f"**Wynik końcowy:** {poprawne} / {len(st.session_state.fiszki_do_nauki)}")

    st.markdown("---")
    # Zapis do statystyki.csv
    nowy_rekord = {
        "id_profilu": st.session_state.id_aktywnego_profilu,
        "data": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "czas": int(czas),
        "typ": tryb,
        "wynik": int(poprawne) if tryb in ["Test", "Trening"] else None,
        "liczba_fiszek": len(st.session_state.fiszki_do_nauki)
    }

    # Dodaj nowy rekord i zapisz
    pd.DataFrame([nowy_rekord]).to_csv("data/statystyki.csv", sep=";", mode="a", header=False, index=False)

    if st.button("Wróć do konfiguracji"):
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

    fraza_zestawu = st.text_input("🔍 Szukaj w swoich zestawach", placeholder="Wpisz nazwę zestawu")

    zestawy_profilu = zestawy_df[zestawy_df["id_profilu"] == st.session_state.id_aktywnego_profilu]

    if fraza_zestawu:
        zestawy_profilu = zestawy_profilu[
            zestawy_profilu["nazwa"].str.contains(fraza_zestawu, case=False, na=False)
        ]
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
    fraza_fiszki = st.text_input("🔍 Szukaj fiszek", placeholder="Wpisz tekst z przodu lub tyłu fiszki")
    
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
        if fraza_fiszki:
            fiszki = fiszki[
                fiszki["przod"].str.contains(fraza_fiszki, case=False, na=False) |
                fiszki["tyl"].str.contains(fraza_fiszki, case=False, na=False)
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
        publiczny = st.checkbox(
        "Publiczny zestaw",
        value=zestaw_do_edycji["publiczny"] if tryb_edycji else False
    )
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
                    zestawy_df.loc[zestawy_df["id"] == zestaw_do_edycji["id"], "publiczny"] = publiczny
                    st.success("Zestaw został pomyślnie zaktualizowany.")
                else:
                    new_id = zestawy_df["id"].max() + 1 if not zestawy_df.empty else 1
                    new_row = pd.DataFrame([{
                        "id": new_id,
                        "nazwa": nazwa,
                        "id_profilu": st.session_state.id_aktywnego_profilu,
                        "publiczny": publiczny
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

    # Jeśli niezalogowany
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
                    st.error("Nieprawidłowy nick lub hasło.")
            else:
                st.error("Nieprawidłowy nick lub hasło.")

        if st.button("Zarejestruj się"):
            st.session_state.aktywna_strona = "Rejestracja"
            st.rerun()

    # Jeśli zalogowany
    elif st.session_state.zalogowany:
        nick = profile_df.loc[profile_df["id"] == st.session_state.id_aktywnego_profilu, "nick"].values[0]

        st.subheader(f"Dane profilu: {nick}")

        #Przycisk edycji
        with st.expander("Edytuj profil"):
            nowy_nick = st.text_input("Nowa nazwa użytkownika", value=nick)
            nowe_haslo = st.text_input("Nowe hasło", type="password")
            potwierdz_haslo = st.text_input("Potwierdź nowe hasło", type="password")

            if st.button("Zapisz zmiany"):
                # Walidacja
                if nowy_nick.strip() == "":
                    st.error("Nazwa użytkownika nie może być pusta.")
                elif nowe_haslo != potwierdz_haslo:
                    st.error("Hasła się nie zgadzają.")
                elif nowy_nick != nick and nowy_nick in profile_df["nick"].values:
                    st.error("Taki użytkownik już istnieje.")
                else:
                    # Aktualizacja
                    profile_df.loc[profile_df["id"] == st.session_state.id_aktywnego_profilu, "nick"] = nowy_nick
                    if nowe_haslo.strip():
                        nowe_haslo_shashowane = hash_haslo(nowe_haslo)
                        profile_df.loc[profile_df["id"] == st.session_state.id_aktywnego_profilu, "haslo"] = nowe_haslo_shashowane

                    # Zapisz
                    profile_df.to_csv("data/profile.csv", sep=";", index=False)

                    st.success("Dane profilu zostały zaktualizowane.")
                    st.session_state.nick = nowy_nick

                st.rerun()

        # Statystyki profilu
        st.subheader("Twoje statystyki:")
        user_stats = statystyki_df[statystyki_df["id_profilu"] == st.session_state.id_aktywnego_profilu]

        liczba_fiszek = fiszki_df[fiszki_df["id_profilu"] == st.session_state.id_aktywnego_profilu].shape[0]
        liczba_zestawow = zestawy_df[zestawy_df["id_profilu"] == st.session_state.id_aktywnego_profilu].shape[0]
        liczba_sesji = user_stats.shape[0]
        suma_czasu = user_stats["czas"].sum()
        sredni_czas = int(user_stats["czas"].mean()) if not user_stats.empty else 0
        testy = user_stats[user_stats["typ"].isin(["Test", "Trening"])].dropna(subset=["wynik"])
        if not testy.empty:
            testy["procent"] = (testy["wynik"] / testy["liczba_fiszek"]) * 100
            sredni_wynik = testy["procent"].mean()
        else:
            sredni_wynik = None

        ostatnia_data = user_stats["data"].max() if not user_stats.empty else "Brak danych"

        st.write(f"Fiszek: **{liczba_fiszek}**")
        st.write(f"Zestawów: **{liczba_zestawow}**")
        st.write(f"Sesji zakończonych: **{liczba_sesji}**")
        st.write(f"Łączny czas nauki: **{suma_czasu//60} min {suma_czasu%60} s**")
        st.write(f"Średni czas sesji: **{sredni_czas//60} min {sredni_czas%60} s**")
        if sredni_wynik is not None:
            st.write(f"Średni wynik: **{sredni_wynik:.1f}%**")
        st.write(f"Ostatnia aktywność: **{ostatnia_data}**")

        # Wylogowywanie
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