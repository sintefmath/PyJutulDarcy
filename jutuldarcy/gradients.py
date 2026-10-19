"""Adjoint sensitivities and optimization with Julia or Python objectives."""

from .julia_import import jl
from .conversion import to_julia, to_python, _kwargs

__all__ = [
    "reservoir_sensitivities",
    "setup_reservoir_parameter_optimization",
    "optimization_config",
    "evaluate_objective",
    "solve_adjoint_sensitivities",
    "npv_objective",
    "setup_reservoir_dict_optimization",
    "parameters_gradient_reservoir",
]


def _objective(function):
    return jl._python_objective(function)


def _gradient_kwargs(kwargs):
    symbols = (
        "mode",
        "method",
        "precond",
        "linear_solver",
        "linear_solver_backend",
        "grad_type",
        "deps",
    )
    kwargs = dict(kwargs)
    for key in ("sim_arg", "simulator_arg", "adjoint_arg"):
        if isinstance(kwargs.get(key), dict):
            kwargs[key] = to_julia(_kwargs(kwargs[key], symbol_keys=symbols))
    return _kwargs(kwargs, symbol_keys=symbols)


def reservoir_sensitivities(case, *args, convert=False, **kwargs):
    """Compute adjoint gradients for objective(model, state, dt, step, forces).

    Pass (case, objective) to simulate first, returning (result, gradients), or
    (case, result, objective) to reuse a forward result. convert=True copies the
    gradient DataDomain to a dict of NumPy arrays. Keep AD values in objectives:
    use Julia arithmetic/reductions and never cast an objective to float.
    """
    if len(args) not in (1, 2):
        raise TypeError("Expected (case, objective) or (case, result, objective)")
    output = jl.JutulDarcy.reservoir_sensitivities(
        case, *args[:-1], _objective(args[-1]), **_gradient_kwargs(kwargs)
    )
    if len(args) == 1:
        result, gradients = output
        return result, to_python(jl._gradient_dict(gradients)) if convert else gradients
    return to_python(jl._gradient_dict(output)) if convert else output


def solve_adjoint_sensitivities(case, result, objective, *, convert=False, **kwargs):
    """Return the lower-level parameter adjoint dictionary."""
    output = jl.Jutul.solve_adjoint_sensitivities(
        case, result, _objective(objective), **_gradient_kwargs(kwargs)
    )
    return to_python(output) if convert else output


def optimization_config(model, parameters=None, *args, **kwargs):
    """Build a Julia optimization config for a case, or model and parameters."""
    if parameters is None:
        return jl.Jutul.optimization_config(model, **_kwargs(kwargs))
    return jl.Jutul.optimization_config(
        model, to_julia(parameters), *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def setup_reservoir_parameter_optimization(case, objective, *args, **kwargs):
    """Return Julia optimization callbacks/configuration (usable from SciPy)."""
    return jl.JutulDarcy.setup_reservoir_parameter_optimization(
        case,
        _objective(objective),
        *(to_julia(a) for a in args),
        **_gradient_kwargs(kwargs),
    )


def evaluate_objective(objective, model, states, dt=None, forces=None, **kwargs):
    """Evaluate an objective with (model, states, dt, forces) or (case, result).

    Passing a ReservoirSimResult includes wells and saved internal timesteps,
    matching the objective used by the adjoint. Its .states field contains only
    reservoir states and is intended for plotting.
    """
    if jl.isa(model, jl.Jutul.JutulCase):
        case = model
        if jl.isa(states, jl.JutulDarcy.ReservoirSimResult):
            states = states.result
        if jl.isa(states, jl.Jutul.SimResult):
            return jl.Jutul.evaluate_objective(
                _objective(objective), case, states, **_kwargs(kwargs)
            )
        model, dt, forces = case.model, case.dt, case.forces
    if jl.isa(states, jl.JutulDarcy.ReservoirSimResult):
        states = states.result
    if jl.isa(states, jl.Jutul.SimResult):
        states, dt, step_index = jl.Jutul.expand_to_ministeps(states)
        kwargs.setdefault("step_index", step_index)
    return jl.Jutul.evaluate_objective(
        _objective(objective),
        model,
        to_julia(states),
        to_julia(dt),
        to_julia(forces),
        **_kwargs(kwargs),
    )


def npv_objective(*args, **kwargs):
    for key in ("injectors", "producers"):
        if key in kwargs:
            kwargs[key] = jl.vect(
                *(jl.Symbol(w) if isinstance(w, str) else w for w in kwargs[key])
            )
    return jl.JutulDarcy.npv_objective(*args, **_kwargs(kwargs))


def setup_reservoir_dict_optimization(*args, **kwargs):
    if isinstance(kwargs.get("parameters"), (list, tuple)):
        kwargs["parameters"] = jl.vect(
            *(jl.Symbol(p) if isinstance(p, str) else p for p in kwargs["parameters"])
        )
    return jl.JutulDarcy.setup_reservoir_dict_optimization(
        *(to_julia(a) for a in args), **_kwargs(kwargs)
    )


def parameters_gradient_reservoir(parameters, objective, *args, **kwargs):
    return jl.JutulDarcy.parameters_gradient_reservoir(
        parameters, _objective(objective), *args, **_gradient_kwargs(kwargs)
    )
