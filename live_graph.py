import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import random
from collections import deque

from subprocess import check_output, CalledProcessError
import time
from datetime import datetime

X = deque(maxlen=20)
Y = deque(maxlen=20)

X.append(1)

host = "8.8.8.8"
time_format = "%H:%M:%S"
timenow = datetime.now().strftime("%Y-%d-%m %H:%M:%S")


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000
        )
    ]
)

@app.callback(Output('live-graph', 'figure'),
              events = [Event('graph-update', 'interval')])
def update_graph():
    try:
        raw_response = check_output(['ping', host, '-n', '1'], universal_newlines=True)

        response = "".join(raw_response).split('=')

        Y.append(response[2].split(' ')[0])
        X.append(X[-1] + 1)

    except CalledProcessError as e:
        Y.append('0')
        X.append(X[-1] + 1)


    data = go.Scatter(
        x = list(X),
        y = list(Y),
        name = 'scatter',
        mode = 'lines+markers',
    )
    return {'data': [data], 'layout': go.Layout(title=f"latency: {response[2].split(' ')[0]} ms", xaxis = dict(range=[min(X), max(X)]),
                                                yaxis = dict(range=[0, int(max(Y)) + 100 ]))}

if __name__ == '__main__':
    app.run_server(debug=True)
