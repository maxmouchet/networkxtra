from networkx.drawing.layout import _process_params, multipartite_layout


def bfs_layout(G, start, center=None, **kwargs):
    """Position nodes according to breadth-first search algorithm.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    start : string
        Starting point.

    center : array-like or None
        Coordinate pair around which to center the layout.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> pos = nx.bfs_layout(G, 0)

    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    """
    from collections import deque

    G, center = _process_params(G, center, 2)
    H = G.copy()  # So original graph remains unmodified

    # Compute layers with BFS
    visited = set()
    queue = deque([(start, 0)])
    while queue:
        current_vertex, current_depth = queue.pop()
        if current_vertex in visited:
            continue
        for nbr in H.neighbors(current_vertex):
            queue.appendleft((nbr, current_depth + 1))
        visited.add(current_vertex)
        H.nodes[current_vertex]["layer"] = current_depth

    # Compute node positions with multipartite_layout
    return multipartite_layout(H, subset_key="layer", **kwargs)
