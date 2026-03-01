import streamlit as st
import pandas as pd
import duckdb
import io

csv = '''
beverage,price
orange juice,2.5
Expresso,2
Tea,3
'''

beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
'''
food_items = pd.read_csv(io.StringIO(csv2))
answer = '''
SELECT *
FROM beverages
CROSS JOIN food_items
'''
solution_df = duckdb.sql(answer)

with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ("Joins","GroupBy","Window function"),
        index=None,
        placeholder="Select a theme..."
    )
    st.write(f"you selected {option}")
st.header("enter your code")
query = st.text_area("Write your SQL request here")
if query :
    result_df = duckdb.query(query).df()
    st.dataframe(result_df)
    try :
        result = result_df[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError :
        st.write("Some columns are missing")

tab1, tab2 = st.tabs(["Tables","Solution"])
with tab1 :
    st.write("Table : beverages")
    st.dataframe(beverages)
    st.write("Table : food_items")
    st.dataframe(food_items)
    st.write("Expected")
    st.dataframe(solution)

with tab2 :
    st.write(answer)
