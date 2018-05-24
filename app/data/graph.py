import json
import time
import os

import dash
import dash_core_components as dcc
import dash_html_components as html

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(base_dir, "data", "ping.json")) as f:
    pingdata = json.load(f)

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Graph(id="example",
              figure= {
                  "data": [
                      {"x": pingdata["time"], "y": pingdata["ping"], "type": "line", "name": "latency",},
                  ],
                  "layout": {
                      "title": "Pingtest",
                      "xaxis": {
                          "title": "tijd",
                          "showticklabels": True,
                          "tick0":0,
                          "dtick":150,
                          "autotick":False,
                      },
                      "yaxis": {
                          "title": "ms",
                      },
                  }
              })
])


if __name__ == "__main__":
    app.run_server(debug=True)
