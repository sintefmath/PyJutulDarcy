from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = [
    "reservoir_domain",
    "number_of_cells",
    "number_of_faces",
    "SourceTerm",
    "FlowBoundaryCondition",
    "flow_boundary_condition",
]


def reservoir_domain(*args, **kwargs):
    """Construct/extract a domain; property matrices are components by cells."""
    return jl.JutulDarcy.reservoir_domain(
        *(to_julia(a, symbols=False) for a in args), **_kwargs(kwargs)
    )


def number_of_cells(*args, **kwargs):
    return int(jl.Jutul.number_of_cells(*args, **kwargs))


def number_of_faces(*args, **kwargs):
    return int(jl.Jutul.number_of_faces(*args, **kwargs))


def SourceTerm(*args, **kwargs):
    if isinstance(kwargs.get("type"), str):
        kwargs["type"] = getattr(jl.JutulDarcy, kwargs["type"])
    return jl.JutulDarcy.SourceTerm(*(to_julia(a) for a in args), **_kwargs(kwargs))


def FlowBoundaryCondition(*args, **kwargs):
    return jl.JutulDarcy.FlowBoundaryCondition(
        *(to_julia(a) for a in args), **_kwargs(kwargs, symbol_keys=("dir",))
    )


def flow_boundary_condition(*args, **kwargs):
    return jl.JutulDarcy.flow_boundary_condition(
        *(to_julia(a) for a in args), **_kwargs(kwargs, symbol_keys=("dir",))
    )
