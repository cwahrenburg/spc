import plotly.express as px
from spc import SPC

feature_id = 1 

def test_chart():
    from config import testDf
    from spc import SPC

    df = SPC(testDf, valueColumn="value", rule2Threshold=2).data

    fig = px.line(
        data_frame= df, 
        x = df.index, 
        y = "value",
        hover_name="sn", 
        markers=True,
    )

    df = df.query("anomoly == True")

    fig.add_trace(
        px.scatter(
            data_frame = df,
            x = df.index,
            y = "value",
            hover_name="sn",
            hover_data=["sn", "anomoly"],
            color_discrete_sequence=["red"]
        )
    ) 
     
    return fig


if __name__ == "__main__": 
    # test_chart().show()
    from config import testDf

    control_chart(SPC(testDf, valueColumn="value", rule2Threshold=2, rule3Threshold=2))