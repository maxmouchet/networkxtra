import networkx as nx
import numpy as np


def to_geojsonl(G, pos, nodes=True, edges=True):
    if nodes:
        for node, data in G.nodes(data=True):
            data = {"node": node, **data}
            feature = {
                "type": "Feature",
                "properties": data,
                "geometry": {
                    "type": "Point",
                    "coordinates": list(np.asarray(pos[node], dtype=np.float64)),
                },
            }
            yield feature

    if edges:
        for u, v, data in G.edges(data=True):
            data = {"u": u, "v": v, **data}
            feature = {
                "type": "Feature",
                "properties": data,
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        list(np.asarray(pos[u], dtype=np.float64)),
                        list(np.asarray(pos[v], dtype=np.float64)),
                    ],
                },
            }
            yield feature


def from_geojsonl(features, create_using=None):
    G = nx.empty_graph(0, create_using)
    for feature in features:
        if feature["geometry"]["type"] == "Point":
            node = feature["properties"].pop("node")
            G.add_node(node, **feature["properties"])
        elif feature["geometry"]["type"] == "LineString":
            u = feature["properties"].pop("u")
            v = feature["properties"].pop("v")
            G.add_edge(u, v, **feature["properties"])
    return G
