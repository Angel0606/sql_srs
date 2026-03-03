# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercices_sql_tables.duckdb",read_only=False)
#-------------------------------#
# EXERCISE LIST TABLE           #
#-------------------------------#
data = {
    "theme": ["cross_joins","cross_joins"],
    "exercise_name":["beverages_and_foods","sizes_and_trademarks"],
    "tables":[["beverages", "food_items"],["sizes","trademarks"]],
    "last_reviewed":["1980-01-01","1970-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state as SELECT * FROM memory_state_df")


#-------------------------------#
# CROSS JOIN EXERCISE           #
#-------------------------------#
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages as SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items as SELECT * FROM food_items")


#-------------------------------#
# CROSS JOIN EXERCISE           #
#-------------------------------#
CSV3 = """
size
XS
S
M
L
XL
"""

sizes = pd.read_csv(io.StringIO(CSV3))
con.execute("CREATE TABLE IF NOT EXISTS sizes as SELECT * FROM sizes")

CSV4 = """
trademark
Nike
Asphalte
Abercrombi
Lewis
"""

trademarks = pd.read_csv(io.StringIO(CSV3))
con.execute("CREATE TABLE IF NOT EXISTS trademarks as SELECT * FROM trademarks")

con.close()