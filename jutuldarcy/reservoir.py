from .julia_import import jl

def reservoir_domain(*arg, **kwargs):
    return jl.reservoir_domain(*arg, **kwargs)
