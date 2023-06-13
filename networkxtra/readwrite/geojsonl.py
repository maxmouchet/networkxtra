import json

from networkx.utils import open_file

from networkxtra.convert.geojsonl import from_geojsonl, to_geojsonl


def generate_geojsonl(G, pos, nodes=True, edges=True):
    for feature in to_geojsonl(G, pos, nodes, edges):
        yield json.dumps(feature)


def parse_geojsonl(lines, create_using=None):
    features = (json.loads(line) for line in lines)
    return from_geojsonl(features, create_using)


@open_file(0, mode="rb")
def read_geojsonl(path, create_using=None, encoding="utf-8"):
    lines = (line if isinstance(line, str) else line.decode(encoding) for line in path)
    return parse_geojsonl(lines, create_using=create_using)


@open_file(2, mode="wb")
def write_geojsonl(G, pos, path, nodes=True, edges=True, encoding="utf-8"):
    for line in generate_geojsonl(G, pos, nodes, edges):
        line += "\n"
        path.write(line.encode(encoding))
