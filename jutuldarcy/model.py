from .julia_import import jl
from .conversion import _stringdict_to_symdict

def setup_reservoir_model(*arg, **kwargs):
    return jl.setup_reservoir_model(*arg, **kwargs)

def reservoir_model(*arg, **kwargs):
    return jl.reservoir_model(*arg, **kwargs)

def setup_reservoir_state(model, first_arg=None, **kwargs):
    if first_arg is None:
        return jl.setup_reservoir_state(model, **kwargs)

    if isinstance(first_arg, list):
        if "EquilibriumRegion" in str(jl.typeof(first_arg[0])):
            first_arg = jl.Vector(first_arg)
    return jl.setup_reservoir_state(model, first_arg, **kwargs)


def setup_reservoir_forces(*arg, control = dict(), limits = dict(), **kwargs):
    control = _stringdict_to_symdict(control)
    limits = _stringdict_to_symdict(limits)
    return jl.setup_reservoir_forces(*arg, control = control, limits = limits, **kwargs)



def EquilibriumRegion(model, *arg, **kwargs):
    return jl.EquilibriumRegion(model, *arg, **kwargs)

def ConstantCompressibilityDensities(*arg, **kwargs):
    return jl.ConstantCompressibilityDensities(*arg, **kwargs)




def replace_variables(model, **kwarg):
    F = jl.seval("replace_variables!")
    F(model, **kwarg)
    return model

def set_secondary_variables(model, model_name=None, **kwarg):
    F = jl.seval("set_secondary_variables!")
    if model_name is None:
        F(model, **kwarg)
    else:
        # If model is a MultiModel, and only one of the models should be updated
        # TODO: Could this function be called with a "SingleModel", or will it always be a MultiModel?
        F(model[jl.Symbol(model_name)], **kwarg)
    return model


