from .julia_import import jl

def si_unit(u):
    """
    Convert a unit to SI unit.
    """
    if isinstance(u, str):
        u = jl.Symbol(u)
    return jl.Jutul.si_unit(u)
