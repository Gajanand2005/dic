import streamlit as st
import sqlite3
from ollama_service import get_meaning

# PAGE CONFIG
st.set_page_config(
    page_title="Hindi Dictionary made by Gagan",
    page_icon="📖",
    layout="centered"
)

# CUSTOM HTML + CSS
st.markdown("""
<style>

body{
    background-color:#0E1117;
}

.main-title{
    text-align:center;
    font-size:45px;
    color:#00ADB5;
    font-weight:bold;
    margin-bottom:10px;
}

.sub-title{
    text-align:center;
    color:white;
    margin-bottom:30px;
}

.result-card{
    background:#1E1E1E;
    padding:20px;
    border-radius:15px;
    margin-top:20px;
    color:white;
    box-shadow:0px 0px 10px rgba(0,255,255,0.2);
}

.history-card{
    background:#1E1E1E;
    padding:15px;
    border-radius:10px;
    margin-top:10px;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# HTML TITLE
st.markdown("""
<div class="main-title">
📖 English to Hindi AI Dictionary
</div>

<div class="sub-title">
Enter your English word and get Hindi meaning, explanation, and example.
</div>
""", unsafe_allow_html=True)

# INPUT
word = st.text_input("Enter English Word")


# SEARCH BUTTON
if st.button("🔍 Search"):

    if word:

        with st.spinner("Searching..."):

            try:

                # AI RESPONSE
                result = get_meaning(word)

                # RESULT CARD
                st.markdown(f"""
                <div class="result-card">

                <h2>📖 {word}</h2>

                <p>{result}</p>

                </div>
                """, unsafe_allow_html=True)

                # DATABASE SAVE
                connection = sqlite3.connect("database.db")
                cursor = connection.cursor()

                cursor.execute(
                    "INSERT INTO history (word, meaning) VALUES (?, ?)",
                    (word, result)
                )

                connection.commit()
                connection.close()

                st.success("Saved in History ✅")

            except Exception as e:

                st.error(f"Error: {e}")

    else:

        st.warning("Please enter a valid word")


# SHOW HISTORY
if st.button("📜 Show History"):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM history ORDER BY id DESC"
    )

    data = cursor.fetchall()

    connection.close()

    st.subheader("📚 Search History")

    for item in data:

        st.markdown(f"""
        <div class="history-card">

        <h4>📖 {item[1]}</h4>

        <p>{item[2]}</p>

        </div>
        """, unsafe_allow_html=True)


# CLEAR HISTORY
if st.button("🗑️ Clear History"):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM history")

    connection.commit()
    connection.close()

    st.success("History Cleared ✅")