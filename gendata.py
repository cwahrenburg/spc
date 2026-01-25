# Script to generate sample data for database

import pandas as pd
from numpy.random import normal
from datetime import datetime
import seaborn as sns

numberOfPoints = 20
measurementsID = 1
values = normal(10, 3, size=10)
created = datetime.now() 
feature_id = 1
machine = "drill"
user_id = 1

def create_values_table():
    df = pd.DataFrame(
        data = {"values" : values}
    )
    df["id"] = measurementsID
    df["created"] = created
    df["feature_id"] = feature_id
    df["machine"] = machine
    df["user_id"] = user_id

    return df

df =create_values_table()

sns.histplot(data = df["values"])
