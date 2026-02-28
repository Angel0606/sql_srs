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
CROSS JOIN food_item
'''
solution = duckdb.sql(answer)

st.header("enter your code")
query = st.text_area("Write your SQL request here",src='user_input')
if query :
    result = duckdb.query(query)
    st.dataframe(result)

tab1, tab2 = st.tabs(["Tables","Solution"])
with tab2 :
    st.write("Table : beverages")
    st.dataframe(beverages)
    st.write("Table : food_items")
    st.dataframe(food_items)
    st.write("Expected")
    st.dataframe(solution)

with tab1 :
    st.write(answer)
