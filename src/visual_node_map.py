import plotly.offline as py

# import chart_studio.plotly as py
import plotly.graph_objs as go
import igraph as ig
import json as js
import sys
import chart_studio


chart_studio.tools.set_credentials_file(
    username="TexnoMan", api_key="AKeVSJCYfS1PYSkrKGPf"
)
filename = sys.argv[1]
f = open(filename, "r", encoding="utf8")
data = js.loads(f.read())

nodes = list(data.keys())
links = dict(data.items())

# Remove nodes with small links
# list_bad_nodes = []
# for n in nodes:
#     d_n = links[n]
#     print(d_n)
#     if d_n['count'] < 2:
#         list_bad_nodes.append()
pop = []
labels = []
Edges = []

N = len(nodes)

for n in nodes:
    d_n = links[n]
    pod_netw = d_n["rel"]
    pod_netw_id = d_n["id"]
    L = len(pod_netw)
    for i in range(0, L):
        Edges.append((d_n["id"], links[pod_netw[i]]["id"]))
    labels.append(n)
    pop.append(int(d_n["count"]))

# print(groups)
G = ig.Graph(Edges, directed=False)

layt = G.layout("kk", dim=3)

Xn = [layt[k][0] for k in range(N)]  # x-coordinates of nodes
Yn = [layt[k][1] for k in range(N)]  # y-coordinates
Zn = [layt[k][2] for k in range(N)]  # z-coordinates
Xe = []
Ye = []
Ze = []
for e in Edges:
    Xe += [layt[e[0]][0], layt[e[1]][0], None]  # x-coordinates of edge ends
    Ye += [layt[e[0]][1], layt[e[1]][1], None]
    Ze += [layt[e[0]][2], layt[e[1]][2], None]

trace1 = go.Scatter3d(
    x=Xe,
    y=Ye,
    z=Ze,
    mode="lines",
    line=dict(color="rgb(125,125,125)", width=1),
    hoverinfo="none",
)

trace2 = go.Scatter3d(
    x=Xn,
    y=Yn,
    z=Zn,
    mode="markers",
    name="actors",
    marker=dict(
        symbol="circle",
        size=pop,
        color=pop,
        colorscale="Viridis",
        line=dict(color="rgb(50,50,50)", width=0.5),
    ),
    text=labels,
    hoverinfo="text",
)

axis = dict(
    showbackground=False,
    showline=False,
    zeroline=False,
    showgrid=False,
    showticklabels=False,
    title="",
)

layout = go.Layout(
    title="Hashtag relative visualization",
    width=1000,
    height=1000,
    showlegend=False,
    scene=dict(
        xaxis=dict(axis),
        yaxis=dict(axis),
        zaxis=dict(axis),
    ),
    margin=dict(t=100),
    hovermode="closest",
    annotations=[
        dict(
            showarrow=False,
            text="Data source: https://www.instagram.com/ ",
            xref="paper",
            yref="paper",
            x=0,
            y=0.1,
            xanchor="left",
            yanchor="bottom",
            font=dict(size=14),
        )
    ],
)

dataB = [trace1, trace2]
fig = go.Figure(data=dataB, layout=layout)

py.iplot(fig, filename="Hash-tag")
