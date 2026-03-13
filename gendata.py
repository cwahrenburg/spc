# Script to generate sample data for database

import pandas as pd
from numpy.random import normal
from datetime import datetime
from dataclasses import dataclass   
from config import CONN
import numpy as np

@dataclass
class Measurement: 
    measurement_id: int
    datapoints: np.array
    feature_id: int
    machine: str
    lsl: float   
    usl: float
    user_id: str = "sys"
    serialNumber: str = "sn"

    def __post_init__(self): 
        self.data = self.create_values_table()

    def create_values_table(self):
        """Generate dataframe which contains all relevant SPC data"""

        df = pd.DataFrame()
        df = pd.DataFrame(data = {"value" : self.datapoints})
        
        df["created"] = datetime.now()
        df["feature_id"] = self.feature_id
        df["machine"] = self.machine
        df["user_id"] = self.user_id
        df["sn"] = self.serialNumber 
        df["usl"] = self.usl
        df["lsl"] = self.lsl

        return df


# Generate Dataset 1
measurements1 = Measurement(
    measurement_id=1,
    datapoints = np.append(normal(10,3,size=100), 22),
    feature_id=1,
    machine="drill",
    lsl = 2.5,
    usl = 15,
    user_id=1,
    serialNumber="abc-123"
)

# Generate out of control point: 
measurements2 = Measurement(
    measurement_id=1,
    datapoints = normal(15,1,size=3),
    feature_id=1,
    machine="drill",
    lsl = 2.5,
    usl = 15,
    user_id=1,
    serialNumber="abc-123"
)


# Feature #2
measurements3 = Measurement(
    measurement_id=2,
    datapoints = normal(0,1,size=100),
    feature_id=2,
    machine="grind",
    lsl = 3,
    usl = -3,
    user_id=1,
    serialNumber="abc-123"
)

measurements4 = Measurement(
    measurement_id=2,
    datapoints=normal(.5, .1, size=15),
    feature_id=2, 
    machine="grind",
    lsl = -3, 
    usl = 3,
    user_id=1,
    serialNumber="abc-1234"

)

measurements5 = Measurement(
    measurement_id=3,
    datapoints=normal(100, 10, size=100),
    feature_id=3, 
    machine="cut",
    lsl = 90, 
    usl = 110,
    user_id=1,
    serialNumber="abc-1234"

)


measurements6 = Measurement(
    measurement_id=3,
    datapoints=np.array([101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114]),
    feature_id=3, 
    machine="cut",
    lsl = 90, 
    usl = 110,
    user_id=1,
    serialNumber="abc-1234"
)

measurements7 = Measurement(
    measurement_id=4, 
    datapoints=np.append(normal(0,1,size=100), [-1, .5, -.5, .25, -2, 1, -3, 3, -1, 2, -1.5, 1, -2, 2.25, -3, 1.1, -2.1, .5, -.5, 2.75]),
    feature_id=4,
    machine = "lathe",
    lsl = -3,
    usl = 3,
    serialNumber="abc-12345" 
)

def write_df_to_db(df): 
    """Write data to database"""

    # Assign data from class to dataframe and write to database
    df.to_sql(
        "measurements",
        CONN,
        if_exists="append", 
        index=False
    )

    print(":) Measurement data successfully generated")

def write_all_measurements_to_database(measurementList):
    """Iterate through list of measurements and write all to database"""
    L = []
    df = pd.DataFrame()
    for measurement in measurementList:
        df = measurement.data
        L.append(measurement.data)

    df = pd.concat(L)
    write_df_to_db(df)
    print("Data copied to database: \n", df)

if __name__ == "__main__": 
    write_all_measurements_to_database([measurements1, measurements2, measurements3, measurements4, measurements5, measurements6, measurements7])
    CONN.commit()
    CONN.close()