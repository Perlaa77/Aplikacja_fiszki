import streamlit as st

st.set_page_config(
    page_title = "Przykład 3"
)

st.subheader("Streamlit posiada wbudowane komunikaty przeznaczone do różnych celów:")

# Komunikat informacyjny
st.info("To jest komunikat informacyjny. Może on powiadamiać użytkownika o dodatkowych użytecznych informacjach.")

# Komunikat sukcesu
st.success("Ten komunikat powiadomi o poprawnym wykonaniu np. pewnej operacji.")

# Komunikat ostrzeżenia
st.warning("Ten komunikat ma być ostrzeżeniem. Prawdopodobnie coś nie jest jak powinno być, ale nie jest to jeszcze błąd.")

# Komunikat błędu
st.error("Tego komunikatu można używać by powiadomić użytkownika o błędach czy niepowodzeniach w działaniu pewnych funkcji.")

st.write("Powyższe komunikaty wykorzystuje się na własne potrzeby, nie muszą się nawet zgadzać z treścią czy faktycznym wykorzystaniem:")
st.warning("Ta wiadomość mogłaby ci powiedzieć, że wszystko wykonało się poprawnie.")

st.markdown("---")

st.write("Poniżej znajduje się specjalny komunikat, wykorzystywany przy obsłudze błędów występujących na poziomie kodu. W przeciwieństwie do pozostałych ma konkretne zadanie, którego nie można zmieniać.")
# Wystąpienie wyjątku
try:
    st.write("Gdy dojdzie do błędu przy wykonywaniu kodu, można taki błąd wyświetlić, np.: gdy próbuje się podzielić liczbę przez 0.")
    x = 1 / 0  # Dzielenie przez zero
    st.write("Gdy wystąpi błąd w 'try', kod umieszczony po tym co wywołało dany błąd się nie wykona.")
# Złapanie błędu dzielenia przez 0
except ZeroDivisionError as e:
    st.exception(e)  # Wyświetlenie błędu i śladu stosu wyjątku