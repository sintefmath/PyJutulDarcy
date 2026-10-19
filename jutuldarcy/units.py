from .julia_import import jl
from .conversion import to_julia

__all__ = ["si_unit", "convert_to_si"]


def si_unit(u):
    """
    Convert a unit to SI unit.
    """
    if isinstance(u, str):
        u = jl.Symbol(u)
    return jl.Jutul.si_unit(u)


def convert_to_si(value, unit):
    if isinstance(unit, str):
        unit = jl.Symbol(unit)
    return jl.convert_to_si(to_julia(value), unit)
