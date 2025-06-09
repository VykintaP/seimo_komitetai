from dash import Input, Output, callback


@callback(Output("selected-committee", "data"), Input("committee-bar", "clickData"))
def store_committee_selection(clickData):
    if clickData and "points" in clickData:
        return clickData["points"][0]["y"]
    return None
