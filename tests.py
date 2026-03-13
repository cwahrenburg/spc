
from cs50 import SQL
from helpers import cs50_query_to_df
import sqlite3
from config import DB
from pprint import pprint
from spc import SPC

def generate_single_control_chart(): 
    df0 = (cs50_query_to_df(qry="SELECT * FROM measurements WHERE machine = 'drill'", DB=DB))

    x = SPC(data=df0, valueColumn="value")
    x.control_chart()
    print(df0.head())
    print(x.data)


def generate_multiple_control_charts(): 
    df0 = cs50_query_to_df(qry="SELECT * FROM measurements", DB=DB)

    for featureID in df0["feature_id"].unique(): 
        chart = SPC(df0.query("feature_id == @featureID"), valueColumn="value")
        print(chart.data)
        chart.control_chart()
        
    
# Run Tests
# generate_single_control_chart()
generate_multiple_control_charts()
