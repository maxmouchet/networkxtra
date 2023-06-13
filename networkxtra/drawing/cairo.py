import io

import cairo
import numpy as np
from networkx import random_layout, rescale_layout

try:
    from tqdm.auto import tqdm
except ImportError:
    pass

IPYTHON = True
try:
    from IPython.display import Image
except ImportError:
    IPYTHON = False


def draw_cairo(
    G,
    pos=None,
    path=None,
    alpha=1.0,
    background_color=(1.0, 1.0, 1.0),
    edge_color=(0.0, 0.0, 0.0),
    linewidths=1.0,
    size=512,
    return_image=True,
    show_progress=False,
):
    if not pos:
        pos = random_layout(G)

    # Rescale layout in [0, size]:
    pos_v = np.array(list(pos.values()))
    pos_v = rescale_layout(pos_v, scale=size / 2) + (size / 2)
    pos = dict(zip(pos, pos_v))

    with cairo.ImageSurface(cairo.Format.RGB24, size, size) as surface:
        ctx = cairo.Context(surface)

        ctx.set_source_rgb(*background_color)
        ctx.rectangle(0, 0, size, size)
        ctx.fill()

        it = enumerate(G.edges())
        if show_progress:
            it = tqdm(it, total=G.number_of_edges())
        for i, (u, v) in it:
            if isinstance(edge_color, list):
                ec = edge_color[i]
            else:
                ec = edge_color
            if isinstance(linewidths, list):
                lw = linewidths[i]
            else:
                lw = linewidths
            ux, uy = pos[u]
            vx, vy = pos[v]
            ctx.set_line_width(lw)
            ctx.set_source_rgba(*ec, alpha)
            ctx.move_to(ux, uy)
            ctx.line_to(vx, vy)
            ctx.stroke()

        if path:
            surface.write_to_png(path)

        if IPYTHON and return_image:
            buffer = io.BytesIO()
            surface.write_to_png(buffer)
            return Image(data=buffer.getbuffer(), format="png")
