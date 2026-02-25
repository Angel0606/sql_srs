import streamlit as st
import pandas as pd
import duckdb

st.write("hello world!!")
data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

input_text = st.text_area(label="Entrer votre requete", value="")
result = duckdb.query(input_text)
st.write(input_text)
#st.dataframe(df)
st.dataframe(result)