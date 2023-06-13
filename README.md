# networkxtra

[![Tests](https://img.shields.io/github/actions/workflow/status/maxmouchet/networkxtra/tests.yml?logo=github)](https://github.com/maxmouchet/networkxtra/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/networkxtra?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/networkxtra/)

Extra functions for [networkx](https://github.com/networkx/networkx):

- Algorithms
  - `largest_connected_component`
- Conversion
  - `from_geojsonl`, `to_geojsonl`
- Drawing
  - `draw_cairo` (much faster than the matplotlib backend)
- Functions
  - `describe(G)`, `remove_leafs(G)`
- Layouts
  - `bfs_layout` (https://github.com/networkx/networkx/pull/5179)
  - `lgl_layout`, `lgl_layout_from_file` (via [minilgl](https://github.com/maxmouchet/minilgl))
- Read/Write
  - `generate_geojsonl`, `parse_geojsonl`, `read_geojsonl`, `write_geojsonl`
  - `generate_lgl`, `parse_lgl`, `read_lgl`, `write_lgl`
