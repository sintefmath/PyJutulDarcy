# PyJutulDarcy

Python access to [JutulDarcy.jl](https://github.com/sintefmath/JutulDarcy.jl).
See the [main documentation](https://sintefmath.github.io/JutulDarcy.jl/dev/)
for physics, model options and examples. This README covers wrapper specifics.

## Installation and Julia environment

```sh
pip install .
```

The `0_4` branch follows the upcoming **JutulDarcy 0.4** on Julia 1.11+.
The repository's `Project.toml` uses `[sources]` to select upstream `main`;
`jutuldarcy/juliapkg.json` declares the same source for automatic installation.
The first `import jutuldarcy` installs/resolves Julia and its packages through
[JuliaPkg](https://github.com/JuliaPy/pyjuliapkg). Use a Python virtual environment
to keep these dependencies isolated. Development source revisions can change.

To use the repository Julia project explicitly, set
`PYTHON_JULIAPKG_PROJECT` to its **absolute directory path** before importing.
JuliaCall's normal environment settings, including `PYTHON_JULIAPKG_EXE` and
`PYTHON_JULIACALL_THREADS`, also apply; set them before the first import.

## Python inputs and outputs

```python
import jutuldarcy as jd

mesh = jd.reservoir_mesh((10, 10, 2), (1000.0, 1000.0, 20.0))
domain = jd.reservoir_domain(mesh, permeability=1e-13, porosity=0.2)

path = jd.test_file_path("SPE9", "SPE9.DATA")  # downloads the example if needed
case = jd.setup_case_from_data_file(path)
result = jd.simulate_reservoir(case)
python_result = jd.convert_to_pydict(result, case, units="field")
```

- Lists, tuples, NumPy arrays, dictionaries and `pathlib.Path` inputs are converted
  to native Julia values. Julia objects remain Julia objects.
- Indices use **Julia's one-based convention**, including cells, well coordinates,
  region numbers and indices into Julia arrays. Python/NumPy outputs use normal
  zero-based indexing. Arrays retain shape: phase/component rows, cell columns.
- Property dictionaries use Symbol keys in Julia. `to_julia(d, symbols=False)`
  preserves strings for parsed DATA/GRDECL dictionaries. `to_python` recursively
  copies Julia dictionaries and numeric arrays to Python/NumPy.
- Simulation returns a Julia `ReservoirSimResult`. `convert=True` returns a Python
  dictionary with `WELLS`, `FIELD`, `DAYS` and `STATES`. Conversion units affect
  summary values; `STATES` retain simulation units. Supply `case` when converting
  a result after `simulate_reservoir`; DATA-file results already retain their case.
- Wrapped mutators omit Julia's `!`: `set_relative_permeability`,
  `set_capillary_pressure`, `replace_variables`, `set_secondary_variables`.
  They return the modified model. Run `setup_parameters(model)` after changing
  property definitions if you keep parameters separately.

The wrapper exposes mesh/domain helpers, states/equilibrium initialization,
well controls and trajectories, sources/boundaries, relperm/Pc tables and
parameter setup. See [examples/standalone.py](examples/standalone.py).
Anything else is accessible through `jd.jl.JutulDarcy`, `jd.jl.Jutul`,
`jd.jl.GeoEnergyIO` and `jd.jl.MultiComponentFlash`; see
[JuliaCall conversions](https://juliapy.github.io/PythonCall.jl/stable/conversion-to-julia/).

## Execution backends

Simulation and `setup_reservoir_simulator` default to `mode="ka"` (CPU).
Strings for Julia options such as `mode`, `method` and `linear_solver` are
converted to Symbols. Pass a Julia `ka_backend` object for custom KA devices.

```python
jd.activate_cuda()  # installs CUDA only if absent; loads it; returns functional()
# Alternatively: jd.activate_amd()
result = jd.simulate_reservoir(case, gpu=True)
simulator, config = jd.setup_reservoir_simulator(case, gpu="cuda")
result = jd.simulate_reservoir(case, simulator=simulator, config=config)
```

`gpu=True` (or `mode="gpu"`) chooses an activated, functional CUDA backend, then AMDGPU. Use
`gpu="cuda"` / `gpu="amd"` or explicit `mode="ka_cuda"` / `mode="ka_amd"`
to select one. A missing/nonfunctional requested GPU raises an error.
`available_backends()` lists usable activated GPUs. `mode="default"` selects
the traditional CPU path. Choose the mode when constructing a simulator.

`remove_cuda()` and `remove_amd()` remove optional JuliaPkg requirements and
disable automatic selection. Restart Python to unload a Julia GPU module.
For device and model limitations, see the
[upstream simulator API](https://sintefmath.github.io/JutulDarcy.jl/dev/man/highlevel/).

## Gradients

```python
def objective(model, state, dt, step, forces):
    pressure = state[jd.jl.Symbol("Reservoir")][jd.jl.Symbol("Pressure")]
    return jd.jl.sum(pressure) * dt

result = jd.simulate_reservoir(case, mode="default", output_substates=True)
gradients = jd.reservoir_sensitivities(case, result, objective, convert=True)
# Or: result, gradients = jd.reservoir_sensitivities(case, objective, convert=True)
```

Python objectives use Julia values, including automatic differentiation values.
Use Julia arithmetic/reductions; casting to `float` or NumPy can discard
derivatives. Julia objective functions are accepted directly too. Gradient keys
such as `"porosity"` and `"permeability"` map to NumPy arrays with `convert=True`;
otherwise the gradient is a Julia DataDomain. Adjoint solves use the host model;
use the CPU path above for forward results reused in an adjoint solve.
Lower-level adjoints, objective evaluation, NPV and parameter optimization setup
are also wrapped. See the
[upstream sensitivity examples](https://sintefmath.github.io/JutulDarcy.jl/dev/).

## Plotting

```python
jd.install_plotting()  # GLMakie; requires an OpenGL-capable display
figure = jd.plot_reservoir(case.model, result)
# In a script, use block=True to wait until the window closes.
```

Plot functions return a Makie figure immediately and accept native results or
Python state dictionaries/lists. Errors propagate with their Julia diagnostics.
For headless rendering:

```python
jd.install_plotting("CairoMakie")
figure = jd.plot_reservoir(case.model, result, display=False, key="Pressure")
jd.jl.CairoMakie.save("pressure.png", figure)
```

`activate_plotting(backend)` loads an already installed backend;
`uninstall_plotting(backend)` removes its requirement. CairoMakie selects the
static reservoir plot automatically.

## Development

```sh
pip install -e '.[test]'
pytest -m 'not plotting'
ruff check jutuldarcy tests examples
```

The tests run real small Julia simulations and compare an adjoint gradient with
finite differences. To test headless plots, install CairoMakie and set
`PYJUTULDARCY_TEST_PLOTTING=1`, then run `pytest -m plotting`. CI covers Linux,
Windows and headless rendering. Examples are Python scripts; notebooks are not
stored in this repository.
