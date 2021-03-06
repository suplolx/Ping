import dash
from dash.dependencies import Output, Input, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import psutil

import lib.utils as utils


mbs_recv = deque(maxlen=20)
mbs_sent = deque(maxlen=20)
latency = deque(maxlen=20)
X = deque(maxlen=20)
X2 = deque(maxlen=20)
X3 = deque(maxlen=20)

X.append(1)
X2.append(1)
X3.append(1)


app = dash.Dash(__name__)

ping = utils.Ping("8.8.8.8")
speed_test = utils.NetSpeed()


app.layout = html.Div([
    html.Div(
        dcc.Graph(id="ping-live-graph", animate=True)
    ),
    html.Div(
    [   
        html.Div(
            dcc.Graph(id="download-live-graph", animate=True),className="six columns"
            ),
        html.Div(
            dcc.Graph(id="upload-live-graph", animate=True),className="six columns"
            ),
        dcc.Interval(
            id="graph-update",
            interval=1000
        )
    ], className="row"
    )
], style={"margin":"auto"})


@app.callback(Output("ping-live-graph", "figure"),
              events = [Event("graph-update", "interval")])
def update_graph():
    response = ping.get_ping()

    if response == "time-out":
        latency.append("0")
        X3.append(X3[-1] + 1)

    else:
        latency.append(response[2].split('ms')[0].strip('<'))
        X3.append(X3[-1] + 1)
      
    data = go.Scatter(
        x = list(X3),
        y = list(latency),
        name = "scatter",
        mode = "lines",
        fill = "tozeroy",
        line = dict(color=("rgb(31, 119, 180)"))
    )
    return {"data": [data], "layout": go.Layout(title="Latency", xaxis = dict(range=[min(X3), max(X3)]),
                                                yaxis = dict(range=[0, int(max(latency)) + 100 ]))}


@app.callback(Output("download-live-graph", "figure"),
                     events= [Event("graph-update", "interval")])
def download_update_graph():
    mbs_recv.append(speed_test.download_speed())

    X.append(X[-1] + 1)

    download_data = go.Scatter(
        x = list(X),
        y = list(mbs_recv),
        name = "Download",
        mode = "lines",
        fill="tozeroy",
        line = dict(color=("rgb(44, 160, 44)"))
    )

    return {
        "data": [download_data],
        "layout": go.Layout(title="Download speed", 
                            xaxis=dict(range=[min(X), max(X)]),
                            yaxis=dict(range=[0, 20]))
    }

@app.callback(Output("upload-live-graph", "figure"),
                     events= [Event("graph-update", "interval")])
def upload_update_graph():
    mbs_sent.append(speed_test.upload_speed())

    X2.append(X2[-1] + 1)

    upload_data = go.Scatter(
        x = list(X),
        y = list(mbs_sent),
        name = "Upload",
        mode = "lines",
        fill="tozeroy",
        line = dict(color=("rgb(255, 127, 14)"))
    )

    return {
        "data": [upload_data],
        "layout": go.Layout(title="Upload speed", 
                            xaxis=dict(range=[min(X2), max(X2)]),
                            yaxis=dict(range=[0, 20]))
    }

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == "__main__":
    app.run_server(debug=True)
