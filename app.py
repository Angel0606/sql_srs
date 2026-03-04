# pylint: disable=missing-module-docstring
import streamlit as st
import duckdb
import os
import subprocess
import logging
from streamlit.logger import get_logger
import sys

def check_user_solution(user_solution: str):
    """
    check that user sql query is correct by
    1 - checking the column
    2 - checking the value
    param user_solution : a string containing the sql query
    """
    result_df = con.execute(user_solution).df()
    st.dataframe(result_df)
    try:
        result = result_df[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError:
        st.write("Some columns are missing")
    nb_lines_diff = result_df.shape[0] - solution_df.shape[0]
    if nb_lines_diff != 0:
        st.write(
            f"result has a {nb_lines_diff} lines difference with the solution"
        )
def select_theme_query(select_theme_user: str = None):
    """
    check that one theme is always selected by
    1 - select the oldest review exercise if nothing selected
    2 - select the oldes review theme if a theme is selected
    return exercise
    param select_theme_user : a string containing the theme if selected, else none
    """
    if select_theme_user:
        select_sql = f"SELECT * FROM memory_state where theme='{select_theme_user}'"
    else:
        select_sql = "SELECT * FROM memory_state"

    exercise = con.execute(select_sql).df() \
        .sort_values("last_reviewed") \
        .reset_index()
    return exercise
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
    theme_available = con.execute("SELECT DISTINCT THEME FROM memory_state").df()
    theme_available_list = theme_available["theme"].unique()
    theme = st.selectbox(
        "What would you like to review ?",
        theme_available_list,
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"you selected {theme}")
    exercise = select_theme_query(theme)
    st.write(exercise)
EXERCISE_NAME = exercise.loc[0, "exercise_name"]
with open(f"answer/{EXERCISE_NAME}.sql", "r") as f:
    answer = f.read()
st.write(answer)
solution_df = con.execute(answer).df()

st.header("enter your code")

query = st.text_area("Write your SQL request here")


if query:
    check_user_solution(query)

tab1, tab2 = st.tabs(["Tables", "Solution"])
with tab1:
    tables_concerned = exercise.loc[0,"tables"]
    for t in tables_concerned:
        st.write(f"table: {t}")
        date_df = con.execute(f"SELECT * FROM {t}").df()
        st.dataframe(date_df)
with tab2:
    st.dataframe(solution_df)
