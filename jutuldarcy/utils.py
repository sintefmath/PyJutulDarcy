from .julia_import import jl
from .conversion import to_julia

__all__ = ["pore_volume", "setup_jutul_case"]


def pore_volume(*args, **kwargs):
    return jl.JutulDarcy.pore_volume(*args, **kwargs)


def setup_jutul_case(state0, model, dt, forces=None, parameters=None, **kwargs):
    """Construct a case; forces and parameters default to the model defaults."""
    if parameters is None:
        parameters = jl.Jutul.setup_parameters(model)
    if forces is None:
        forces = jl.JutulDarcy.setup_reservoir_forces(model)
    return jl.Jutul.JutulCase(
        model,
        to_julia(dt),
        to_julia(forces),
        state0=to_julia(state0),
        parameters=to_julia(parameters),
        **kwargs,
    )
