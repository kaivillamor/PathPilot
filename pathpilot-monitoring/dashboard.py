import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import os


app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        html.Div(dcc.Graph(id="response-times-graph"), style={"width": "50%"}),
        html.Div(dcc.Graph(id="degree-searches-graph"), style={"width": "50%"}),
    ], style={"display": "flex"}),
    html.Div([
        html.Div(dcc.Graph(id="total-requests-graph"), style={"width": "50%"}),
        html.Div(dcc.Graph(id="error-count-graph"), style={"width": "50%"}),
    ], style={"display": "flex"}),
    dcc.Interval(id="interval", interval=5000, n_intervals=0)
])

@app.callback(
    Output("response-times-graph", "figure"),
    Output("total-requests-graph", "figure"),
    Output("degree-searches-graph", "figure"),
    Output("error-count-graph", "figure"),
    Input("interval", "n_intervals")
)

def update_graphs(n):
    secret = os.getenv("METRICS_SECRET", "")
    data = requests.get("http://backend:5000/metrics", headers={"X-Metrics-Secret": secret}).json()

    response_times_figure = go.Figure(
        go.Scatter(
            x = [r["time"] for r in data["response_times"]],
            y = [r["value"] for r in data["response_times"]]
        )
    )
    response_times_figure.update_layout(title = "Response Times")

    total_requests_figure = go.Figure(
        go.Indicator(
            mode="number",
            value=data["total_requests"],
            title={"text": "Degree Searches<br><span style='font-size:0.6em;color:gray'>1 search = 1 USAJobs call + 1 TheirStack call</span>"}
        )
    )

    degree_figure = go.Figure(
        go.Bar(
            x=list(data["degree_searches"].keys()),
            y=list(data["degree_searches"].values())
        )
    )
    degree_figure.update_layout(title="Searches by Degree")

    breakdown = data.get("error_breakdown", {})
    error_count_figure = go.Figure(
        go.Bar(
            x=list(breakdown.keys()) if breakdown else ["No errors"],
            y=list(breakdown.values()) if breakdown else [0],
            marker_color=["#e74c3c" if k != "No errors" else "#2ecc71" for k in (breakdown.keys() if breakdown else ["No errors"])]
        )
    )
    error_count_figure.update_layout(
        title=f"API Errors by Source (Total: {data['error_count']})",
        xaxis_title="Source",
        yaxis_title="Count"
    )

    return response_times_figure, total_requests_figure, degree_figure, error_count_figure

# note that the port is 8050 as the default for dash
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8050)