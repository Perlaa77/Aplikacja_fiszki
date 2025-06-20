import streamlit as st
import pandas as pd # Biblioteka Pandas

st.set_page_config(
    page_title = "Przykład 9",
    layout="wide"
)

st.header("Pandas to biblioteka, którą można łączyć ze Streamlit do łatwiejszej edycji i wyświetlania danych.")

# File uploader pozwala na wybranie i załadowanie pliku o odpowiednim formacie
uploaded_file = st.file_uploader(label="Wybierz plik CSV", type="csv")

# Reszta elementów wyświetli się, gdy zostanie wybrany plik
if uploaded_file:

    # Załadowanie danych z wybranego pliku CSV do formatu DataFrame
    dataframe = pd.read_csv(uploaded_file, sep=';') # Jako separator wybrany został średnik

    st.subheader("Wyświetlenie danych w formie interaktywnej tabeli")
    # Interaktywna tabelka
    st.dataframe(dataframe)

    st.subheader("Wyświetlenie danych w formie statycznej tabeli opisującej kolumny liczbowe")
    # Statyczna tabelka
    st.table(dataframe.describe())

    st.subheader("Wyświetlenie danych w formie wykresu słupkowego zliczającego wystąpienia danych w wybranej kolumnie")
    column = st.selectbox("Wybierz kolumnę do zliczeń:", dataframe.columns)
    # Wykres słupkowy
    st.bar_chart(dataframe[column].value_counts())

    st.subheader("Wyświetlenie danych w formie mapy")
    column_latitude = [column for column in dataframe.columns if 'latitude' in column.lower()]
    column_longitude = [column for column in dataframe.columns if 'longitude' in column.lower()]
    if column_latitude and column_longitude:
        map_dataframe = dataframe[[column_latitude[0], column_longitude[0]]].dropna()
        map_dataframe.columns = ['latitude', 'longitude']

        # Dane ukazane na mapie
        st.map(map_dataframe)
    else:
        st.error("Brak odpowiednich danych w pliku - mapa nie może zostać pokazana.")

    st.subheader("Pobieranie danych")
    # Przycisk do pobrania danych w formacie CSV
    st.download_button("Pobierz dane jako plik CSV", data=dataframe.to_csv(index=False).encode('utf-8'), file_name="data.csv", mime="text/csv")

else:
    st.write("Wybierz przygotowany plik przykładowy 'data_9.csv', aby zobaczyć możliwości łączenia Streamlit z Pandas.")