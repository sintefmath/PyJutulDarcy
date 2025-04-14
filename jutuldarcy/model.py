from .julia_import import jl
from .conversion import _stringdict_to_symdict

def setup_reservoir_model(*arg, **kwargs):
    return jl.setup_reservoir_model(*arg, **kwargs)

def setup_reservoir_state(*arg, **kwargs):
    return jl.setup_reservoir_state(*arg, **kwargs)

def setup_reservoir_forces(*arg, controls = dict(), limits = dict(), **kwargs):
    controls = _stringdict_to_symdict(controls)
    limits = _stringdict_to_symdict(limits)
    return jl.setup_reservoir_forces(*arg, **kwargs)
