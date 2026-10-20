"""Simulation entry points; KernelAbstractions on CPU is the default."""

from .julia_import import jl
from .conversion import to_julia, convert_to_pydict, _convert_units
from .backends import _simulation_kwargs

__all__ = ["simulate_data_file", "simulate_reservoir", "setup_reservoir_simulator"]


def simulate_data_file(
    data_file_name, *, convert=False, units=jl.missing, mode="default", gpu=False, **kwargs
):
    """Simulate a DATA path or parsed deck; gpu=True selects an activated GPU."""
    units = _convert_units(units)
    result = jl.JutulDarcy.simulate_data_file(
        to_julia(data_file_name, symbols=False),
        **_simulation_kwargs(mode, gpu, **kwargs),
    )
    return convert_to_pydict(result, units=units) if convert else result


def simulate_reservoir(
    *args, convert=False, units=jl.missing, mode="ka", gpu=False, **kwargs
):
    """Simulate a case or (state0, model, dt); optionally return Python results."""
    units = _convert_units(units)
    # A supplied simulator/config already determines the execution backend.
    if "simulator" in kwargs:
        if gpu or mode != "ka":
            raise ValueError(
                "Select mode/gpu when constructing the supplied simulator."
            )
        from .conversion import _kwargs

        options = _kwargs(kwargs)
    else:
        options = _simulation_kwargs(mode, gpu, **kwargs)
    converted = tuple(to_julia(arg) for arg in args)
    result = jl.JutulDarcy.simulate_reservoir(*converted, **options)
    if not convert:
        return result
    if len(converted) == 1:
        case = converted[0]
    else:
        from .utils import setup_jutul_case

        case = setup_jutul_case(
            *converted, forces=kwargs.get("forces"), parameters=kwargs.get("parameters")
        )
    return convert_to_pydict(result, case, units=units)


def setup_reservoir_simulator(*args, mode="ka", gpu=False, **kwargs):
    """Return (simulator, config). Supports mode='ka_*' and Julia ka_backend objects."""
    return jl.JutulDarcy.setup_reservoir_simulator(
        *(to_julia(arg) for arg in args), **_simulation_kwargs(mode, gpu, **kwargs)
    )
