from .julia_import import jl

def setup_vertical_well(*arg, name = "Well", **kwargs):
    if isinstance(name, str):
        name = jl.Symbol(name)
    return jl.setup_vertical_well(*arg, name = name, **kwargs)

def setup_well(*arg, name = "Well", **kwargs):
    if isinstance(name, str):
        name = jl.Symbol(name)
    return jl.setup_well(*arg, name = name, **kwargs)
