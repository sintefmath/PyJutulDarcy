"""Optional Julia GPU packages and simulator execution modes."""

import juliapkg

from .julia_import import jl

__all__ = [
    "activate_cuda",
    "activate_amd",
    "remove_cuda",
    "remove_amd",
    "available_backends",
]

_PACKAGES = {
    "cuda": ("CUDA", "052768ef-5323-5732-b1bb-66c8b64840ba"),
    "amd": ("AMDGPU", "21141c5a-9bdb-4563-92ae-f87d6854732e"),
}
_enabled = set()


def _activate(backend):
    name, uuid = _PACKAGES[backend]
    if not jl._package_present(name):
        juliapkg.add(name, uuid)
        juliapkg.resolve()
    jl._load_optional_package(name, uuid)
    _enabled.add(backend)
    return bool(getattr(jl, name).functional())


def activate_cuda():
    """Add CUDA only if absent, load it, and return CUDA.functional()."""
    return _activate("cuda")


def activate_amd():
    """Add AMDGPU only if absent, load it, and return AMDGPU.functional()."""
    return _activate("amd")


def _remove(backend):
    name, _ = _PACKAGES[backend]
    _enabled.discard(backend)
    juliapkg.rm(name)
    jl._remove_optional_package(name)
    juliapkg.resolve()
    return True


def remove_cuda():
    """Remove the CUDA requirement. Restart Python to unload Julia modules."""
    return _remove("cuda")


def remove_amd():
    """Remove the AMDGPU requirement. Restart Python to unload Julia modules."""
    return _remove("amd")


def available_backends():
    """Return activated, functional GPUs, in CUDA then AMD order."""
    return [
        key
        for key, (name, _) in _PACKAGES.items()
        if key in _enabled and bool(getattr(jl, name).functional())
    ]


def _simulation_kwargs(mode="ka", gpu=False, **kwargs):
    if isinstance(mode, str):
        mode = mode.lower()
        if mode == "gpu":
            mode, gpu = "ka", gpu or True
    if gpu:
        if mode != "ka":
            raise ValueError("Use mode='ka' with gpu, or select an explicit ka_* mode.")
        choices = available_backends()
        selected = choices[0] if choices else None
        if isinstance(gpu, str):
            selected = {"amdgpu": "amd", "nvidia": "cuda"}.get(gpu.lower(), gpu.lower())
        if selected not in choices:
            raise RuntimeError(
                "No requested functional GPU backend. Call activate_cuda() or activate_amd() first."
            )
        mode = f"ka_{selected}"
    if mode in ("ka_cuda", "ka_amd"):
        selected = mode.removeprefix("ka_")
        if selected not in available_backends():
            raise RuntimeError(
                f"Activate a functional {selected} backend before selecting {mode}."
            )
    from .conversion import _kwargs

    kwargs = _kwargs(
        kwargs,
        symbol_keys=(
            "method",
            "precond",
            "linear_solver",
            "linear_solver_backend",
            "timesteps",
            "transport_scheme",
        ),
    )
    kwargs["mode"] = jl.Symbol(mode) if isinstance(mode, str) else mode
    return kwargs
