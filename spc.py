from dataclasses import dataclass

import pandas as pd
import numpy as np
import plotly.express as px

@dataclass
class SPC:
    """Class to define control chart rules and basic statistics"""
    data: pd.DataFrame
    valueColumn: str
    databaseIDCol:str = "measurement_id"
    featureNameCol = "feature"
    machineNameCol = "machine"
    featureIDColName = "feature_id"
    lslCol: str = None
    uslCol: str = None
    rule2Threshold: int = 9
    rule3Threshold: int = 6
    rule4Threshold: int = 14

    def __post_init__(self): 

        # Convert series to dataframe
        self.values = pd.DataFrame(self.data[self.valueColumn])

        # Calculate basic statistics
        self._calc_mean()
        self._calc_sigma()
        self._calc_spec_limits()
        self._calc_control_limits()
        self._calc_zones()

        # Calc Performance 
        self._calc_spec_limits
        self._calc_yield()
        self._calc_ppk()
        self._calc_all_metrics()

        # Control chart rules:
        self._rule1()
        self._rule2()
        self._rule3()
        self._rule4()
        self.list_rule_violations()
        self.return_data()

    # Basic statistics used in quantifying control chart behavior 
    def _calc_mean(self): 
        self.mean = self.values["value"].mean()

    def _calc_sigma(self): 
        self.sigma = self.values["value"].std()

    def _calc_spec_limits(self): 
        self.usl = self.data["usl"].iloc[0]
        self.lsl = self.data["lsl"].iloc[0]

    def _calc_yield(self): 
        df = self.data

        df["in_spec"] = df[self.valueColumn].apply(lambda x: True if self.lsl < x < self.usl else False)
        self.fpy = df["in_spec"].sum() / df["in_spec"].count()

        self.data = df

    def _calc_ppk(self): 
        self.pp_upper = (self.usl - self.mean) / (3 * self.sigma)
        self.pp_lower = (self.mean - self.lsl) / (3 * self.sigma)
        self.ppk = min(self.pp_upper, self.pp_lower)

    def _calc_control_limits(self):
        self.ucl = self.mean + 3 * self.sigma
        self.lcl = self.mean - 3 * self.sigma

    def _calc_all_metrics(self):
        data = {
            "feature_id": self.data[self.featureIDColName].iloc[0],
            "Machine": self.data[self.machineNameCol].iloc[0],
            "Mean" : self.mean,
            "Std.Dev": [self.sigma],
            "USL": [self.usl],
            "LSL": [self.lsl],
            "FPY": [self.fpy],
            "ppl": [self.pp_lower],
            "ppu": [self.pp_upper],
            "ppk": [self.ppk],
        }
        df = pd.DataFrame(data)
        self.metrics = df.copy()
        
    def _calc_zones(self): 
        self.zones = {
            "1" : [self.mean + 1 * (self.sigma), self.mean -1 * (self.sigma)],
            "2" : [self.mean + 2 * (self.sigma), self.mean -2 * (self.sigma)],
            "3" : [self.mean + 3 * (self.sigma), self.mean -3 * (self.sigma)],
            }

    # Calculate control chart rules
    def _rule1(self):
        """Any point more than 3 standard deviations away from mean"""
        self.values["rule1v"] = self.values["value"].apply(
            lambda x: True if (x > self.mean+3*self.sigma or x < self.mean - 3*self.sigma) else False)

    def _rule2(self): 
        """nine points in a row on the same side of mean"""
        
        self.values["greater or less than mean"] = self.values["value"].apply(lambda x: "greater" if x > self.mean else "less")

        # Inspired by NBA streak data analysis https://joshdevlin.com/blog/calculate-streaks-in-pandas/
        
        # 1) Identify start of "streak" of points
        self.values["start of streak"] = self.values["greater or less than mean"].ne(self.values["greater or less than mean"].shift())

        # 2) Create a unique idenfifier which increments one every time a new streak begins
        self.values["streak_id"] = self.values["start of streak"].cumsum()
        
        # TODO: This is confusing - how does groupby get added as a separate column?
        # 3) Groupby "streak_id" and cumulative count occurrances of streak_id and add 1 since count starts at zero 
        self.values["streak_counter"] = self.values.groupby("streak_id").cumcount() + 1

        # Apply rule for any points of streak counter which are 9 in a row
        self.values["rule2v"] = self.values["streak_counter"].apply(lambda x: True if x >=  self.rule2Threshold else False)
        
        # Drop Columns other than "rule2v"
        self.values.drop(columns = ["greater or less than mean", "streak_id", "streak_counter", "start of streak"], inplace=True)

    def _rule3(self): 
        """six points in a row all increasing or decreasing"""
        
        df = self.values
        
        df["diff"] = df["value"].diff()

        def increasing_or_decreasing(x): 
            if x > 0: 
                return "increasing"
            elif x < 0: 
                return "decreasing"
            else: 
                return 
            
        df["increasing or decreasing"] = df["diff"].apply(increasing_or_decreasing)

        # 1. Start of streak points: 
        df["start of streak"] = df["increasing or decreasing"].ne(df["increasing or decreasing"].shift())

        # 2) Create a unique idenfifier which increments one every time a new streak begins
        df["streak_id"] = df["start of streak"].cumsum()
        
        # 3) Groupby "streak_id" and cumulative count occurrances of streak_id and add 1 since count starts at zero 
        df["streak_counter"] = df.groupby("streak_id").cumcount() + 1

        # 4) Apply Rule to streak id
        df["rule3v"] = df["streak_counter"].apply(lambda x: True if x >= self.rule3Threshold else False)

        # Drop Columns other than "rule2v"
        df.drop(columns = ["increasing or decreasing", "streak_id", "streak_counter", "start of streak"], inplace=True)
        

        self.values = df

    def _rule4(self): 
        """Fourteen points in a row alternating up or down"""
         
        df = self.values
        
        # Flag alternating points
        df["diff"] = df["value"] - df["value"].shift()

        def increasing_or_decreasing_int(x): 
            if x > 0: 
                return 1
            elif x < 0: 
                return -1
            else: 
                return 0 
            
        df["increasing or decreasing"] = df["diff"].apply(increasing_or_decreasing_int)

        df["alternating"] = df["increasing or decreasing"] + df["increasing or decreasing"].shift(1)

        df["alternating tf"] = df["alternating"].apply(lambda x: True if x == 0 else False)

        # # 1. Start of streak points: 
        df["start of streak"] = df["alternating tf"].ne(df["alternating tf"].shift(1))

        def start_of_alternating_streak(alternating:float, start_of_streak:bool): 
            if alternating != 0: 
                return False
            if start_of_streak == True and alternating == 0: 
                return True
            else: 
                return False

        df["start of alternating streak"] = df.apply(lambda x: start_of_alternating_streak(x["alternating"], x["start of streak"]), axis=1)

        # 2) Create a unique idenfifier which increments one every time a new streak begins
        df["streak_id"] = df["start of alternating streak"].cumsum()

        # 2a) Everywhere where the points are not alternating, set that streak_id to nothing to prevent false flags
        df.loc[df["alternating"] != 0, "streak_id"] = np.nan

        # 3) Groupby "streak_id" and cumulative count occurrances of streak_id and add 1 since count starts at zero 
        df["streak_counter"] = df.groupby("streak_id").cumcount() + 1

        # 4) Apply rule for any points of streak counter which are greater than threshold
        df["rule4v"] = df["streak_counter"].apply(lambda x: True if x >= self.rule4Threshold else False)

        df.drop(columns=["diff", "increasing or decreasing", "start of streak", "start of alternating streak", "streak_id", "alternating", "alternating tf", "streak_counter"], inplace=True)

        self.values = df
    
    def list_rule_violations(self):

        df = self.values

        def generate_list_of_violations(rule1v, rule2v, rule3v, rule4v): 
            rule_violations = []

            if rule1v == True: 
                rule_violations.append("1")
            if rule2v == True: 
                rule_violations.append("2")
            if rule3v == True: 
                rule_violations.append("3")
            if rule4v == True: 
                rule_violations.append("4")
            
            return rule_violations

        df["rule_violations"] = df.apply(lambda x: generate_list_of_violations(x["rule1v"], x["rule2v"], x["rule3v"], x["rule4v"]), axis=1)

        df["anomoly"] = df["rule_violations"].apply(lambda x: True if x != [] else False)
        self.values = df

    def return_data(self): 
        df = self.values
        df = self.values.iloc[:,[-1, -2]]
        self.return_data = df
        self.data = pd.concat([self.data, df], axis='columns')

    def control_chart(self):
        
        # Store SPC class data into easy access df
        df = self.data

        machineID = df["machine"].iloc[0]
        featureID = df["feature_id"].iloc[0]

        hoverDataList = ["measurement_id", "value", "anomoly", "rule_violations", "note_text"]

        fig = px.line(
            data_frame=df,
            x = df.index,
            y = "value",
            color_discrete_sequence=["black"], 
            markers=True, 
            title = f"Machine: {machineID} / Feature: {featureID}", 
            hover_name="measurement_id",
            hover_data = hoverDataList
        )

        # Plot Anomolies as discrete points on top of line chart. 
        # Do not plot anything if there are no anomolies detected: 
        anomolies = df.query("anomoly == True")

        if not anomolies.empty:
            fig.add_trace(
                px.scatter(
                    data_frame=anomolies, 
                    x = anomolies.index, 
                    y = "value", 
                    color_discrete_sequence=["crimson"],
                    hover_data=hoverDataList,
                    hover_name="measurement_id"
                ).data[0]
            )
            fig.update_traces(marker = dict(size=12, line=dict(width=1)))

        # Overlay Note points
        notePoints = df.query("note_text.notnull()", engine="python")

        if not notePoints.empty:
            fig.add_trace(
                px.scatter(
                    data_frame=notePoints, 
                    x = notePoints.index, 
                    y = "value", 
                    color_discrete_sequence=["yellow"],
                    hover_data=hoverDataList,
                    hover_name="measurement_id"
                ).data[0]
            )
            fig.update_traces(marker = dict(size=12, line=dict(width=1)))



        # Plot Sigma Lines
        fig.add_hline(self.mean, line_dash="dash")
        fig.add_hline(self.ucl)
        fig.add_hline(self.lcl)
            
        # Add a little spacing for plot beyond control limits. 
        paddingAmt = .10
        ymin = min([df["value"].min(), self.lcl])*(1-paddingAmt)
        ymax = max([df["value"].max(), self.ucl])*(1+paddingAmt)
        fig.update_yaxes(range=[ymin, ymax])

        # Display Final Figure
        # fig.show()
        return fig

if __name__ == "__main__":
    
    from helpers import cs50_query_to_df
    from config import DB
    from config import qryMeasurementSQL

    df = cs50_query_to_df(qry=qryMeasurementSQL, DB=DB)
    df = df.query("feature_id == 4.0")

    test = SPC(data=df, valueColumn="value")
    print(test.data.head)
    print(test.usl)

