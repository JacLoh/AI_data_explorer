# app.py
import os
import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from config import DB_CONFIG
from db.mysql_manager import init_db, insert_prompt, insert_feedback, fetch_prompts
from services.ai_service import answer_question
from utils.file_handler import parse_file


PORT = os.getenv("PORT", 8501)

try:
    init_db()
except Exception as e:
    st.error(f"MySQL connection failed: {e}")

if "dataframes" not in st.session_state:
    st.session_state.dataframes = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = None

st.title("📊 AI-Powered CSV/XLS Data Explorer")

# === FILE UPLOAD ===
uploaded_files = st.file_uploader("Upload CSV or XLS files", type=["csv", "xls", "xlsx"], accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        df = parse_file(uploaded_file)
        st.session_state.dataframes[uploaded_file.name] = df
    st.success("Files uploaded successfully!")

# === FILE SELECTION ===
if st.session_state.dataframes:
    file_names = list(st.session_state.dataframes.keys())
    selected_file = st.selectbox("Select a file to explore", file_names)
    st.session_state.selected_file = selected_file

    df = st.session_state.dataframes[selected_file]

    n = st.number_input("Show top N rows", min_value=1, value=5)
    st.dataframe(df.head(n))

    # === Ask Question ===
    st.subheader("💬 Ask a question about this data")
    question = st.text_input("Enter your question")
    if st.button("Get Answer") and question:
        try:
            answer = answer_question(df, question)
            st.write("### 🤖 Answer:", answer)

            prompt_id = str(uuid.uuid4())
            insert_prompt(prompt_id, selected_file, question, str(answer), datetime.now())

            st.markdown("---")
            st.subheader("📝 Was this answer helpful?")
            rating = st.radio("", ["👍 Yes", "👎 No"], horizontal=True)
            comment = st.text_area("Any comments?")
            if st.button("Submit Feedback"):
                insert_feedback(str(uuid.uuid4()), prompt_id, rating, comment, datetime.now())
                st.success("Feedback submitted. Thank you!")
        except Exception as e:
            st.error(f"Error: {e}")

# === PROMPT HISTORY ===
st.sidebar.title("🕓 Prompt History")
prompts = fetch_prompts(limit=10)
for filename, question, answer, timestamp in prompts:
    with st.sidebar.expander(f"{question} ({filename})"):
        st.write(f"**Answer:** {answer}")
        st.caption(f"Asked on: {timestamp}")
