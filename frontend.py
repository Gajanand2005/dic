import streamlit as st
import sqlite3
from ollama_service import get_meaning

st.title("Hindi Dictionary")
st.set_page_config(
    page_title="Hindi Dictionary made by Gagan",
    page_icon="📃",
    layout="centered"
)

st.title("English to Hindi Dictionary made by Gagan 📃")
st.markdown("Enter you English Word and find the hindi word and meaning and example")


word = st.text_input("Enter English word")

if st.button("Search"):

    if word:

        with st.spinner("Searching..."):

            try:
                # Get AI response
                result = get_meaning(word)

                # Show result
                st.subheader("Meaning")
                st.write(result)

                # Save in database
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO history (word, meaning) VALUES (?, ?)",
                    (word, result)
                )

                connection.commit()
                connection.close()

                st.success("Saved in history")

            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.warning("Please enter a valid word")


if st.button("📃 Show History"):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM history")
    data = cursor.fetchall()
    
    connection.close()
    
    st.subheader("Search History")
    
    for item in data:
        st.write(f"word:{item[1]}")
        st.write(f"meaning:{item[2]}")
        st.write(f"...................")

if st.button("🗑️ Clear History"):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM history")

    connection.commit()
    connection.close()

    st.success("History Cleared")