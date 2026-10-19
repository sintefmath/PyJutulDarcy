"""Makie plots return their figure immediately; block=True waits in scripts."""

import asyncio
import time

import juliacall
import juliapkg

from .julia_import import jl
from .conversion import to_julia, _kwargs

__all__ = [
    "activate_plotting",
    "install_plotting",
    "uninstall_plotting",
    "plot_reservoir",
    "plot_well_results",
    "plot_field_measurables",
    "plot_reservoir_measurables",
    "plot_summary",
    "make_interactive",
    "plot_async",
]

_BACKENDS = {
    "GLMakie": "e9467ef8-e4e7-5192-8a1a-b1aee30e663a",
    "CairoMakie": "13f3f980-e62b-5c42-98c6-ff1f3baf88f0",
}
_backend = None
_tasks = set()


def activate_plotting(backend="GLMakie"):
    """Load an installed Makie backend. CairoMakie supports headless rendering."""
    if backend not in _BACKENDS:
        raise ValueError(f"Unknown plotting backend {backend!r}")
    module = jl._load_optional_package(backend, _BACKENDS[backend])
    getattr(module, "activate!")()
    global _backend
    _backend = backend
    return True


def install_plotting(backend="GLMakie"):
    if backend not in _BACKENDS:
        raise ValueError(f"Unknown plotting backend {backend!r}")
    if not jl._package_present(backend):
        juliapkg.add(backend, _BACKENDS[backend])
        juliapkg.resolve()
    return activate_plotting(backend)


def uninstall_plotting(backend="GLMakie"):
    if backend not in _BACKENDS:
        raise ValueError(f"Unknown plotting backend {backend!r}")
    juliapkg.rm(backend)
    jl._remove_optional_package(backend)
    juliapkg.resolve()
    global _backend
    if _backend == backend:
        _backend = None
    return True


def _plot(function, *args, display=True, block=False, **kwargs):
    if _backend is None:
        activate_plotting()
    if block and (not display or _backend != "GLMakie"):
        raise ValueError("block=True requires display=True and GLMakie")
    output = function(*(to_julia(a) for a in args), **_kwargs(kwargs))
    # The fancy reservoir explorer returns a struct with .fig, other plots a Figure.
    figure = output.fig if jl.hasproperty(output, jl.Symbol("fig")) else output
    if display:
        jl.display(figure)
    if block:
        while jl.isopen(figure.scene):
            jl.seval("yield()")
            time.sleep(0.01)
    elif display and _backend == "GLMakie":
        make_interactive()
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            pass
        else:
            task = loop.create_task(_keep_alive(figure))
            _tasks.add(task)
            task.add_done_callback(_tasks.discard)
    return figure


async def _keep_alive(figure):
    while jl.isopen(figure.scene):
        jl.seval("yield()")
        await asyncio.sleep(0.01)


def plot_reservoir(*args, **kwargs):
    """Return the Makie figure for a case/model/domain and optional states/result.

    With CairoMakie, gui=False and force_glmakie=False are the defaults.
    Python state dictionaries/lists are converted to native Julia containers.
    """
    if _backend == "CairoMakie":
        kwargs.setdefault("gui", False)
        kwargs.setdefault("force_glmakie", False)
    return _plot(jl.JutulDarcy.plot_reservoir, *args, **kwargs)


def plot_well_results(*args, **kwargs):
    return _plot(jl.JutulDarcy.plot_well_results, *args, **kwargs)


def plot_field_measurables(*args, **kwargs):
    """Compatibility alias for JutulDarcy's plot_reservoir_measurables."""
    return plot_reservoir_measurables(*args, **kwargs)


def plot_reservoir_measurables(*args, **kwargs):
    return _plot(jl.JutulDarcy.plot_reservoir_measurables, *args, **kwargs)


def plot_summary(*args, **kwargs):
    return _plot(jl.JutulDarcy.plot_summary, *args, **kwargs)


def make_interactive():
    """Integrate Julia's event loop for non-blocking GLMakie windows."""
    return juliacall.interactive()


def plot_async(function, *args, **kwargs):
    """Compatibility entry point; return the figure without owning an asyncio loop."""
    return _plot(function, *args, **kwargs)
