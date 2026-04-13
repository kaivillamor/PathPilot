import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id = "response-times-graph"),
    dcc.Graph(id = "total-requests-graph"),
    dcc.Graph(id = "degree-searches-graph"),
    dcc.Graph(id = "error-count-graph"),
    dcc.Interval(id = "interval", interval = 5000, n_intervals = 0)
])

@app.callback(
    Output("response-times-graph", "figure"),
    Output("total-requests-graph", "figure"),
    Output("degree-searches-graph", "figure"),
    Output("error-count-graph", "figure"),
    Input("interval", "n_intervals")
)

def update_graphs(n):
    data = requests.get("http://backend:5000/metrics").json()

    response_times_figure = go.Figure(
        go.Scatter(
            x = [r["time"] for r in data["response_times"]],
            y = [r["value"] for r in data["response_times"]]
        )
    )
    response_times_figure.update_layout(title = "Response Times")

    total_requests_figure = go.Figure(
        go.Indicator(
            mode = "number",
            value = data["total_requests"],
            title = {"text": "Total Requests"}
        )
    )

    degree_figure = go.Figure(
        go.Bar(
            x = list(data["degree_searches"].keys()),
            y = list(data["degree_searches"].values())
        )
    )
    degree_figure.update_layout(title = "Degree Searches")

    error_count_figure = go.Figure(
        go.Indicator(
            mode = "number",
            value = data["error_count"],
            title = {"text": "Error Count"}
        )
    )

    return response_times_figure, total_requests_figure, degree_figure, error_count_figure

# note that the port is 8050 as the default for dash
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8050)