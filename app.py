# pylint: disable=missing-module-docstring
import streamlit as st
import duckdb
import os
import subprocess
import logging
from streamlit.logger import get_logger
import sys

app_logger = get_logger(__name__)
app_logger.setLevel(logging.WARNING) # ici on peut mettre DEBUG, ERROR, WARNING, INFO

if "data" not in os.listdir():
    app_logger.info("need to create data folder")
    os.mkdir("data")
if "exercices_sql_tables.duckb" not in os.listdir("data"):
    app_logger.info("need to create Database and tables")
    subprocess.run([f"{sys.executable}", "init_db.py"], check=False)
con = duckdb.connect(database="data/exercices_sql_tables.duckdb",read_only=False)
with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"you selected {theme}")
    if theme:
        select_sql = f"SELECT * FROM memory_state where theme='{theme}'"
    else:
        select_sql = "SELECT * FROM memory_state"

    exercise = con.execute(select_sql).df()\
                .sort_values("last_reviewed")\
                .reset_index()
    st.write(exercise)
EXERCISE_NAME = exercise.loc[0, "exercise_name"]
with open(f"answer/{EXERCISE_NAME}.sql", "r") as f:
    answer = f.read()
st.write(answer)
solution_df = con.execute(answer).df()

st.header("enter your code")

query = st.text_area("Write your SQL request here")
if query:
    result_df = con.execute(query).df()
    st.dataframe(result_df)
    try:
        result = result_df[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing")

tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    tables_concerned = exercise.loc[0,"tables"]
    for t in tables_concerned:
        st.write(f"table: {t}")
        date_df = con.execute(f"SELECT * FROM {t}").df()
        st.dataframe(date_df)
with tab2:
    st.dataframe(solution_df)
