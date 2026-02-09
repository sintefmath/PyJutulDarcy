from .julia_import import jl

def pore_volume(*arg, **kwargs):
    return jl.pore_volume(*arg, **kwargs)

def setup_jutul_case(state0, model, dt, forces, *args):
    """
    Setup a Jutul case (a self-contained simulation case) with the given model,
    time step, forces, and parameters.
    """
    if len(args) == 0:
        parameters = jl.setup_parameters(model)
    else:
        parameters = args[0]

    return jl.JutulCase(model, dt, forces, state0 = state0, parameters = parameters)
