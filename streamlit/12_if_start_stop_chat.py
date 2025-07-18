import streamlit as st

st.set_page_config(
    page_title = "Przykład 12"
)


# Tytuł aplikacji
st.title("Demo funkcji Streamlit")

# Przykład użycia "if"
st.subheader("Przykład: instrukcja warunkowa `if`")
x = st.number_input("Podaj liczbę", value=0)

if x > 0:
    st.success("Liczba jest dodatnia!")
elif x < 0:
    st.warning("Liczba jest ujemna.")
else:
    st.info("Liczba to zero.")

# Przykład użycia st.stop()
st.subheader("Przykład: `st.stop()`")

if st.checkbox("Zatrzymaj program tutaj"):
    st.write("Program został zatrzymany przed dalszym kodem.")
    st.stop()

st.write("Ten kod wykonuje się tylko, jeśli `stop()` nie został uruchomiony.")

# Przykład użycia st.rerun()
st.subheader("Przykład: `st.rerun()`")

if st.button("Uruchom ponownie aplikację"):
    st.write("Aplikacja zostanie uruchomiona ponownie.")
    st.rerun()

# Przykład użycia czatu: chat_input + chat_message
st.subheader("Przykład: Chat z użytkownikiem")

# Wyświetlenie wiadomości systemowej (np. od "bota")
with st.chat_message("assistant"):
    st.write("Cześć! Jak mogę Ci pomóc?")

# Pobieranie wiadomości od użytkownika
user_input = st.chat_input("Napisz coś:")

# Jeśli użytkownik coś wpisze, wyświetlamy jego wiadomość i odpowiedź
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        st.write(f"Odpowiedź bota: Napisałeś '{user_input}'.")
