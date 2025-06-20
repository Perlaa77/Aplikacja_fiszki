# Aby uruchomić program wykorzystujący Streamlit należy w konsoli wpisać: streamlit run <nazwa_pliku>.py
# Np. do uruchomienia tego kodu należy wpisać: streamlit run 1_streamlit.py
# Należy pamiętać, że w konsoli trzeba znajdować się w tym samym katalogu co program, który chce się uruchomić.

# Import Streamlit
import streamlit as st

# Konfiguracja strony - (jeśli używana) musi być wywołana przed jakimkolwiek innym poleceniem Streamlit
st.set_page_config(
    page_title = "Przykład 1", # Nazwa strony, wyświetlana w zakładce przeglądarki
    page_icon = "🙂", # Favicon, wyświetlany w zakładce obok nazwy strony
    layout = "wide", # Układ: 'centered' - wyśrodkowany lub 'wide' - szeroki/od lewego brzegu
    initial_sidebar_state = "auto", # Jeśli używany jest boczny pasek nawigacyjny, ustawia jego stan początkowy
    menu_items = { # Edycja menu w prawym górnym rogu ,domyślna przyjmuje 'None'
        # Można nadpisać elementy: "Get help", "Report a bug" oraz "About"
        "About": "To jest jeden z elementów menu, który można nadpisać."
    }
)

# Tytuł
st.title("To jest tytuł rozdziału i twojej przygody ze Streamlit!")

# Nagłówek
st.header("A to jest nagłówek.")

# Nagłówek podrzędny - podnagłówek
st.subheader("Ten podnagłówek jest mniejszy od nagłówka.")

# Użycie markdown do otrzymania poziomej linii - więcej o tym w dalszym przykładzie
st.markdown("---")

st.header("Tytuły, nagłówki i nagłówki podrzędne pozwalają w przejrzysty sposób oddzielić od siebie różne informacje...")
st.title("...a także wskazać na ich istotność.")
st.subheader("Mogą występować wielokrotnie na stronie.")

my_list = ["truskawka", "banan", "arbuz"] # Deklaracja listy
number = 21 # Deklaracja zmiennej
st.markdown("---")

# Wypisywanie tekstu na stronie
st.write("Za pomocą 'write' można wypisywać na ekranie różne informacje. \nW 'write' nie działają '\\n'.")
st.write("Trzeba użyć kolejnego 'write' do rozpoczęcia kolejnego akapitu czy uzyskania nowej linii z większym odstępem.")
st.write("Można tu jednak wyświetlać sformatowane np.: listy:", my_list, "czy zmienne: ", number, " - dzięki temu, że write przyjmuje wiele argumentów.")
st.text("Tekst można także wyświetlać z pomocą 'text',\ntutaj '\\n' działają. Nie można jednak wyświetlać list czy innych obiektów tak jak w 'write'.")
st.text(f"Zarówno w 'text' jak i w 'write' można wyświetlać zmienne w środku tekstu: x = {number}, dodając literę 'f' przed cudzysłowem i używając klamer.")