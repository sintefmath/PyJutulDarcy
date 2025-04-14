from .julia_import import jl

def pore_volume(*arg, **kwargs):
    return jl.pore_volume(*arg, **kwargs)
