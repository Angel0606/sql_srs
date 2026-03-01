# pylint: disable=missing-module-docstring
import streamlit as st
import duckdb

# ANSWER = """
# SELECT *
# FROM beverages
# CROSS JOIN food_items
# """
# solution_df = duckdb.sql(ANSWER)
con = duckdb.connect(database="data/exercices_sql_tables.duckdb",read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write(f"you selected {theme}")
    exercise = con.execute(f"SELECT * FROM memory_state where theme='{theme}'").df()
    st.write(exercise)
st.header("enter your code")

query = st.text_area("Write your SQL request here")
# if query:
#     result_df = duckdb.query(query).df()
#     st.dataframe(result_df)
#     try:
#         result = result_df[solution_df.columns]
#         st.dataframe(result.compare(solution_df))
#     except KeyError:
#         st.write("Some columns are missing")

# tab1, tab2 = st.tabs(["Tables", "Solution"])
# with tab1:
#     st.write("Table : beverages")
#     st.dataframe(beverages)
#     st.write("Table : food_items")
#     st.dataframe(food_items)
#     st.write("Expected")
#     st.dataframe(solution_df)
#
# with tab2:
#     st.write(ANSWER)
