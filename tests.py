
from cs50 import SQL
from helpers import cs50_query_to_df
import sqlite3
from config import DB
from pprint import pprint
from spc import SPC
import pandas as pd
from config import qryMeasurementSQL
from helpers import add_note_to_measurement

sql =  "SELECT * FROM measurements JOIN features ON features.id = measurements.feature_id;"

def general_query(): 
    df = cs50_query_to_df(qry=qryMeasurementSQL, DB=DB)
    print(df)

def generate_single_control_chart(): 
    df0 = (cs50_query_to_df(qry="SELECT * FROM measurements WHERE machine = 'drill'", DB=DB))

    x = SPC(data=df0, valueColumn="value")
    x.control_chart()
    print(df0.head())
    print(x.data)


def generate_multiple_control_charts():

    df0 = cs50_query_to_df(qry=sql, DB=DB)

    for featureID in df0["feature_id"].unique(): 
        chart = SPC(df0.query("feature_id == @featureID"), valueColumn="value", uslCol="usl", lslCol="lsl")
        print(chart.data)
        chart.control_chart().show()
        
def test_metrics(): 
    df = cs50_query_to_df(qry = sql, DB=DB)

    L = [] 
    for featureID in df["feature_id"].unique():
        print(featureID)
        spc = SPC(df.query("feature_id == @featureID").copy(), valueColumn="value", uslCol="usl", lslCol="lsl")
        L.append(spc.metrics)

    metrics = pd.concat(L).reset_index()
    print(metrics)

# Run Tests
# generate_single_control_chart()
# generate_multiple_control_charts()

# test_metrics()
# general_query()

def test_add_note():
    add_note_to_measurement(13773, "this is a test of the function")

test_add_note()