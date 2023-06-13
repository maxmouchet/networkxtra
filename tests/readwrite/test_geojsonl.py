import networkx as nx

from networkxtra import read_geojsonl, write_geojsonl


def test_read_write_geojsonl(tmp_path):
    expected = nx.random_regular_graph(5, 100)
    pos = nx.random_layout(expected)
    write_geojsonl(expected, pos, tmp_path / "graph.lgl")
    actual = read_geojsonl(tmp_path / "graph.lgl")
    assert actual.nodes == expected.nodes
    assert actual.edges == expected.edges
