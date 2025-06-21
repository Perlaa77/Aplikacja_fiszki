import streamlit as st
import pydeck as pdk
import pandas as pd

# Ustawienie tytułu aplikacji
st.title("Mapa z punktami przy użyciu Pydeck")

# Pydeck to wysokopoziomowe API do tworzenia interaktywnych map WebGL,
# oparte na deck.gl (biblioteka od Ubera).
# Pozwala tworzyć warstwy wizualizacyjne, np. punkty, kolumny, linie, heksagony itp.
# W Streamlit integruje się przez komponent `st.pydeck_chart`.

# Przykładowe dane: lista punktów z szerokością i długością geograficzną
data = pd.DataFrame({
    'lat': [52.2297, 50.0614, 51.1079],  # Warszawa, Kraków, Wrocław
    'lon': [21.0122, 19.9383, 17.0385],
    'city': ['Warszawa', 'Kraków', 'Wrocław']
})

# Wyświetlenie tabeli z danymi
st.subheader("Dane lokalizacji")
st.dataframe(data)

# Tworzenie warstwy punktów przy użyciu ScatterplotLayer (kropki na mapie)
layer = pdk.Layer(
    "ScatterplotLayer",        # Typ warstwy do wizualizacji punktów
    data=data,                 # Źródło danych (DataFrame)
    get_position='[lon, lat]',# Wyrażenie JS określające pozycję punktu
    get_color='[200, 30, 0, 160]',  # Kolor punktu (czerwony z przezroczystością)
    get_radius=10000,          # Rozmiar punktu w metrach
    pickable=True              # Umożliwia wyświetlanie podpowiedzi po najechaniu
)

# Ustawienie początkowego widoku kamery mapy (środek i zoom)
view_state = pdk.ViewState(
    latitude=data['lat'].mean(),    # Ustawienie środka mapy (średnia szerokość)
    longitude=data['lon'].mean(),   # Ustawienie środka mapy (średnia długość)
    zoom=5,                         # Poziom przybliżenia
    pitch=40                        # Kąt nachylenia kamery (do efektu 3D)
)

# Tworzenie obiektu Deck, który łączy warstwy i widok
deck = pdk.Deck(
    layers=[layer],                      # Lista warstw (tu tylko jedna)
    initial_view_state=view_state,      # Widok początkowy mapy
    tooltip={"text": "Miasto: {city}"}  # Podpowiedź wyświetlana po najechaniu
)

# Wyświetlenie mapy w Streamlit
st.subheader("Interaktywna mapa Pydeck")
st.pydeck_chart(deck)
