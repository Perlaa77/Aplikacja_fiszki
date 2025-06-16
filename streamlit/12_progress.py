import streamlit as st
import time # Do upływu czasu

st.set_page_config(
    page_title = "Przykład 12",
    layout="wide"
)

st.subheader("Za pomocą 'toast' można aktywować wyskakujące powiadomienia.")
st.write("Pokażą się na boku ekranu i same znikną po pewnym czasie.")

# Przycisk uruchamiający wyskakujące powiadomienie
if st.button("Pokaż powiadomienie"):
    st.toast("Oto powiadomienie!")


st.subheader("Przy wykonywaniu się kodu zajmującego trochę czasu można wykorzystać kilka wizualnych elementów, które będą informować, że operacje się wciąż wykonują w tle.")

# Przycisk uruchamiający spinner
if st.button("Spinner"):

    # Spinner jest uruchamiany z pomocą słowa 'with' i pokazuje się tak długo, aż nie wykonają się wszystkie operacje wewnątrz 'with'
    with st.spinner("Myślenie..."):

        time.sleep(5) # Poczekaj 5 sekund
    st.write("Przemyślano.")

# Przycisk uruchamiający pasek postępu
if st.button("Pasek postępu"):

    # Uruchomienie paska z wartością początkową w zakresie od 0 do 100, pasek ma być przypisany do zmiennej, aby mógł się zmieniać
    p = st.progress(0)

    for i in range(100):
        time.sleep(0.05)
        p.progress(i + 1) # Aktualizacja paska postępu
    st.write("Pasek się wypełnił.")

st.progress(50) # Pasek na stałe wypełniony do połowy

# Przycisk uruchamiający postępy ze statusem
if st.button("Status postępu"):

    # Tak jak spinner używany z 'with'
    with st.status("Przetwarzanie...", expanded=True, state="running") as status:

        st.write("Zrób coś i poczekaj")
        time.sleep(2)
        st.write("Pomyśl jeszcze chwilę")
        time.sleep(2)
        st.write("Koniec")

        # Aktualizacja statusu po zakończeniu działań
        status.update(label="Proces zakończony", state="complete")