import networkx as nx
from networkx import NetworkXNotImplemented


def largest_connected_component(G):
    try:
        return max(nx.connected_components(G), key=len)
    except NetworkXNotImplemented:
        return max(nx.weakly_connected_components(G), key=len)
