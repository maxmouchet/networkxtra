import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from networkx.drawing.layout import _process_params, rescale_layout
from networkx.utils import open_file

from networkxtra.readwrite.lgl import write_lgl


def lgl_layout(
    G,
    scale=1,
    center=None,
    dim=2,
    init_mass=None,
    init_pos=None,
    threads=None,
    max_iterations=None,
    neighborhood_radius=None,
    timestep=None,
    node_radius=None,
    node_mass=None,
    outer_perim_radius=None,
    root_node=None,
    tree_only=False,
    quiet=True,
    equilibrium_distance=None,
    ellipse_factors=None,
    placement_distance=None,
    placement_radius=None,
    place_leafs_close_by=False,
    timeout=None,
):
    assert dim in (2, 3)
    G, center = _process_params(G, center, dim)
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        graph_file = tmpdir / "input.lgl"
        write_lgl(G, graph_file)
        mass_file = tmpdir / "init_mass.txt"
        if init_mass:
            mass_file.write_text(
                "\n".join(f"{node} {mass}" for node, mass in sorted(init_mass.items()))
            )
        pos_file = tmpdir / "init_pos.txt"
        if init_pos:
            pos_file.write_text(
                "\n".join(
                    f"{node} {' '.join(str(x) for x in pos)}"
                    for node, pos in sorted(init_pos.items())
                )
            )
        exe = "lglayout2d" if dim == 2 else "lglayout3d"
        cmd = [exe]
        if init_mass:
            cmd += ["-m", str(mass_file)]
        if init_pos:
            cmd += ["-x", str(pos_file)]
        if threads:
            cmd += ["-t", str(threads)]
        if max_iterations:
            cmd += ["-i", str(max_iterations)]
        if neighborhood_radius:
            cmd += ["-r", str(neighborhood_radius)]
        if timestep:
            cmd += ["-T", str(timestep)]
        if node_radius:
            cmd += ["-S", str(node_radius)]
        if node_mass:
            cmd += ["-M", str(node_mass)]
        if outer_perim_radius:
            cmd += ["-R", str(outer_perim_radius)]
        if root_node:
            cmd += ["-z", str(root_node)]
        if tree_only:
            cmd += ["-y"]
        if quiet:
            cmd += ["-I"]
        if equilibrium_distance:
            cmd += ["-q", str(equilibrium_distance)]
        if ellipse_factors:
            cmd += ["-E", str(ellipse_factors)]
        if placement_distance:
            cmd += ["-u", str(placement_distance)]
        if placement_radius:
            cmd += ["-v", str(placement_radius)]
        if place_leafs_close_by:
            cmd += ["-L"]
        cmd += [str(graph_file)]
        subprocess.run(
            cmd, capture_output=quiet, check=True, cwd=tmpdir, timeout=timeout
        )
        layout_file = tmpdir / "lgl.out"
        return lgl_layout_from_file(layout_file, scale=scale, center=center)


@open_file(0, "rb")
def lgl_layout_from_file(path, scale=1, center=None, encoding="utf-8"):
    nodes, pos = [], []
    lines = (line if isinstance(line, str) else line.decode(encoding) for line in path)
    for line in lines:
        node, *coords = line.split(" ")
        coords = [float(x) for x in coords]
        if any(x >= 1e6 for x in coords):
            continue
        try:
            node = int(node)
        except ValueError:
            pass
        nodes.append(node)
        pos.append(coords)
    if center is None:
        center = np.zeros(len(pos[0]))
    else:
        center = np.asarray(center)
    pos = np.array(pos)
    pos = rescale_layout(pos, scale=scale) + center
    return dict(zip(nodes, pos))
