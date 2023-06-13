import networkx as nx
from networkx.utils import open_file


def generate_lgl(G):
    for node, neighbors in G.adjacency():
        yield f"# {node}"
        yield from (str(x) for x in neighbors)


def parse_lgl(lines, create_using=None):
    G = nx.empty_graph(0, create_using)
    source = None
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            source = line[2:]
            try:
                source = int(source)
            except ValueError:
                pass
            G.add_node(source)
        else:
            try:
                line = int(line)
            except ValueError:
                pass
            G.add_edge(source, line)
    return G


@open_file(0, mode="rb")
def read_lgl(path, create_using=None, encoding="utf-8"):
    lines = (line if isinstance(line, str) else line.decode(encoding) for line in path)
    return parse_lgl(lines, create_using=create_using)


@open_file(1, mode="wb")
def write_lgl(G, path, encoding="utf-8"):
    for line in generate_lgl(G):
        line += "\n"
        path.write(line.encode(encoding))
