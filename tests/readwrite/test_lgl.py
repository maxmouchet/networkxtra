import networkx as nx

from networkxtra import read_lgl, write_lgl


def test_read_write_lgl(tmp_path):
    expected = nx.random_regular_graph(5, 100)
    write_lgl(expected, tmp_path / "graph.lgl")
    actual = read_lgl(tmp_path / "graph.lgl")
    assert actual.nodes == expected.nodes
    assert actual.edges == expected.edges
