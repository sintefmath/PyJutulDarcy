from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = [
    "LiquidPhase",
    "VaporPhase",
    "AqueousPhase",
    "ImmiscibleSystem",
    "SinglePhaseSystem",
]


def LiquidPhase():
    return jl.JutulDarcy.LiquidPhase()


def VaporPhase():
    return jl.JutulDarcy.VaporPhase()


def AqueousPhase():
    return jl.JutulDarcy.AqueousPhase()


def ImmiscibleSystem(phases, **kwargs):
    if isinstance(phases, list):
        phases = tuple(phases)
    return jl.JutulDarcy.ImmiscibleSystem(to_julia(phases), **_kwargs(kwargs))


def SinglePhaseSystem(*args, **kwargs):
    return jl.JutulDarcy.SinglePhaseSystem(
        *(to_julia(a) for a in args), **_kwargs(kwargs)
    )
