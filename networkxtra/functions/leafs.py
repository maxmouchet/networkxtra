def remove_leafs(G):
    leafs = [node for node in G.nodes() if G.out_degree(node) == 0]
    G.remove_nodes_from(leafs)
