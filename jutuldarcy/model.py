from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = [
    "setup_reservoir_model",
    "reservoir_model",
    "setup_reservoir_state",
    "setup_reservoir_forces",
    "EquilibriumRegion",
    "ConstantCompressibilityDensities",
    "replace_variables",
    "set_secondary_variables",
    "setup_parameters",
]


def setup_reservoir_model(*args, **kwargs):
    args = list(args)
    if len(args) > 1 and isinstance(args[1], str):
        args[1] = jl.Symbol(args[1])
    return jl.JutulDarcy.setup_reservoir_model(
        *(to_julia(a) for a in args), **_kwargs(kwargs, symbol_keys=("backend",))
    )


def reservoir_model(*args, **kwargs):
    return jl.JutulDarcy.reservoir_model(*args, **kwargs)


def setup_reservoir_state(model, first_arg=None, **kwargs):
    args = () if first_arg is None else (to_julia(first_arg),)
    return jl.JutulDarcy.setup_reservoir_state(model, *args, **_kwargs(kwargs))


def setup_reservoir_forces(model, *, control=None, limits=None, **kwargs):
    return jl.JutulDarcy.setup_reservoir_forces(
        model, control=to_julia(control), limits=to_julia(limits), **_kwargs(kwargs)
    )


def EquilibriumRegion(model, *args, **kwargs):
    return jl.JutulDarcy.EquilibriumRegion(
        model, *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def ConstantCompressibilityDensities(*args, **kwargs):
    return jl.JutulDarcy.ConstantCompressibilityDensities(
        *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def replace_variables(model, **kwargs):
    getattr(jl.Jutul, "replace_variables!")(model, **_kwargs(kwargs))
    return model


def set_secondary_variables(model, model_name=None, **kwargs):
    target = model if model_name is None else model[jl.Symbol(model_name)]
    getattr(jl.Jutul, "set_secondary_variables!")(target, **_kwargs(kwargs))
    return model


def setup_parameters(model, **kwargs):
    return jl.Jutul.setup_parameters(model, **_kwargs(kwargs))
