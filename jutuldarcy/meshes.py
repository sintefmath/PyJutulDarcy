from numbers import Real

import numpy as np

from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = ["CartesianMesh", "UnstructuredMesh", "reservoir_mesh", "extract_submesh"]


def CartesianMesh(dims, *args, **kwargs):
    """Construct a Julia Cartesian mesh from Python dimensions and lengths."""
    if isinstance(dims, (list, tuple, np.ndarray)):
        dims = tuple(int(v) for v in dims)
    args = list(args)
    if args and isinstance(args[0], (list, tuple, np.ndarray)):
        args[0] = tuple(float(v) if isinstance(v, Real) else v for v in args[0])
    return jl.Jutul.CartesianMesh(
        to_julia(dims), *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def UnstructuredMesh(*args, **kwargs):
    return jl.Jutul.UnstructuredMesh(*(to_julia(a) for a in args), **_kwargs(kwargs))


def reservoir_mesh(*args, **kwargs):
    """Construct or extract a reservoir mesh; accepts tuples, grid dicts and cases."""
    args = list(args)
    offset = int(bool(args) and isinstance(args[0], str))
    if len(args) > offset and isinstance(args[offset], (list, np.ndarray)):
        args[offset] = tuple(int(v) for v in args[offset])
    if len(args) > offset + 1 and isinstance(
        args[offset + 1], (list, tuple, np.ndarray)
    ):
        args[offset + 1] = tuple(
            float(v) if isinstance(v, Real) else v for v in args[offset + 1]
        )
    return jl.JutulDarcy.reservoir_mesh(
        *(to_julia(a, symbols=False) for a in args), **_kwargs(kwargs)
    )


def extract_submesh(mesh, cells, **kwargs):
    """Extract cells specified using Julia's one-based cell indices."""
    return jl.Jutul.extract_submesh(mesh, to_julia(cells), **_kwargs(kwargs))
