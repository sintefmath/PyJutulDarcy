from .julia_import import jl
from .conversion import _stringdict_to_symdict

def setup_reservoir_model(*arg, **kwargs):
    return jl.setup_reservoir_model(*arg, **kwargs)

def setup_reservoir_state(*arg, **kwargs):
    return jl.setup_reservoir_state(*arg, **kwargs)

def setup_reservoir_forces(*arg, control = dict(), limits = dict(), **kwargs):
    control = _stringdict_to_symdict(control)
    limits = _stringdict_to_symdict(limits)
    return jl.setup_reservoir_forces(*arg, control = control, limits = limits, **kwargs)

def replace_variables(model, **kwarg):
    F = jl.seval("replace_variables!")
    F(model, **kwarg)
    return model
