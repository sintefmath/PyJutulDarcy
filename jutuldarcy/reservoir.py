from .julia_import import jl

def reservoir_domain(*arg, **kwargs):
    return jl.reservoir_domain(*arg, **kwargs)

def number_of_cells(*arg, **kwargs):
    return jl.number_of_cells(*arg, **kwargs)
