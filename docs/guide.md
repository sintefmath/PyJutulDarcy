# User guide

## Cases and results

Keep the Julia case and result when you need geometry, model parameters, plots
or gradients. Convert the result when working with NumPy or Python plotting:

```python
import jutuldarcy as jd

case = jd.setup_case_from_data_file("MODEL.DATA")
result = jd.simulate_reservoir(case)
output = jd.convert_to_pydict(result, case, units="field")
```

| Converted entry | Contents |
| --- | --- |
| `FIELD` | Summary names such as `FOPR`, mapped to NumPy arrays |
| `WELLS` | Well names, each mapped to a dictionary of summary arrays |
| `DAYS` | Output times in days |
| `STATES` | One dictionary of reservoir arrays per output time |

`units` accepts `"si"`, `"metric"`, `"field"` or `"lab"` for summaries.
State arrays retain SI units. `simulate_data_file(..., convert=True)` combines
setup, simulation and conversion. Its native result retains the case; for
`simulate_reservoir` results, pass the case when converting separately.

To reuse a simulator, select the backend when constructing it:

```python
simulator, config = jd.setup_reservoir_simulator(case, mode="ka")
result = jd.simulate_reservoir(case, simulator=simulator, config=config)
```

See the [Julia high-level API](https://sintefmath.github.io/JutulDarcy.jl/stable/man/highlevel/)
for timestep, solver and output options.

## Python and Julia values

- Wrapper inputs accept lists, tuples, dictionaries, NumPy arrays and `Path`s.
  Numerical arrays are copied into Julia and retain their shape. Multiphase
  arrays normally have shape **(phases, cells)**.
- **Cell indices, well coordinates and regions are one-based**, as in Julia.
  Indexing JuliaCall arrays *from Python* and converted NumPy arrays is zero-based:
  `result.states[0]` is the first reporting step.
- Dictionary keys become Julia `Symbol`s recursively. Use
  `jd.to_julia(data, symbols=False)` for string-keyed dictionaries. DATA/GRDECL
  parsing wrappers handle this automatically.
- Models, domains, wells and cases remain Julia objects. `jd.to_python(value)`
  recursively copies Julia dictionaries and arrays into Python/NumPy.

```python
state = jd.to_julia({"Pressure": [1e7, 1e7, 1e7]})
pressure = state[jd.jl.Symbol("Pressure")]
python_state = jd.to_python(state)
```

Functions without a wrapper are available through `jd.jl.JutulDarcy`,
`jd.jl.Jutul`, `jd.jl.GeoEnergyIO` and `jd.jl.MultiComponentFlash`. Direct calls
may require explicit conversions. Access names ending in `!` with `getattr`:

```python
getattr(jd.jl.Jutul, "replace_variables!")(model, PhaseMassDensities=density)
# Wrapped equivalent:
jd.replace_variables(model, PhaseMassDensities=density)
```

After changing property definitions, recreate any separately stored parameters
with `jd.setup_parameters(model)`. See
[JuliaCall conversions](https://juliapy.github.io/PythonCall.jl/stable/conversion-to-julia/)
for direct interoperation.

## CPU and GPU execution

| Selection | Execution |
| --- | --- |
| Default, `mode="ka"` or `mode="ka_cpu"` | KernelAbstractions CPU kernels |
| `mode="ka_cpu_static"` | CPU kernels with static scheduling |
| `mode="default"` | Traditional CPU simulator; use for adjoints |
| `gpu=True` or `mode="gpu"` | First activated, functional GPU: CUDA, then AMDGPU |
| `gpu="cuda"` or `mode="ka_cuda"` | CUDA |
| `gpu="amd"` or `mode="ka_amd"` | AMDGPU |

GPU packages are optional. Activate them explicitly before requesting a GPU:

```python
if jd.activate_cuda():  # Or jd.activate_amd(). Installs the Julia package if absent.
    result = jd.simulate_reservoir(case, gpu=True)
```

`jd.available_backends()` lists activated, functional GPUs. An unavailable
requested GPU raises an error. `jd.remove_cuda()` / `jd.remove_amd()` remove
their requirements; restart Python to unload Julia modules. Custom Julia devices
can be passed as `ka_backend` with `mode="ka"`. See
[Julia GPU support](https://sintefmath.github.io/JutulDarcy.jl/stable/man/advanced/gpu)
for hardware and model restrictions.

## Plotting

For static images on servers or in CI, install CairoMakie once:

```python
jd.install_plotting("CairoMakie")
figure = jd.plot_reservoir(case.model, result, display=False, key="Pressure")
jd.jl.CairoMakie.save("pressure.png", figure)
```

For interactive windows, use `jd.install_plotting()` to install GLMakie. This
requires an OpenGL-capable display. `jd.plot_reservoir(case.model, result)`
returns immediately in a REPL or running asyncio loop. Use `block=True` in a
script to keep the window open until closed. `activate_plotting(backend)` loads
an already installed backend. See the [executed plotting example](examples/plots.md)
and [Julia plotting guide](https://sintefmath.github.io/JutulDarcy.jl/stable/man/basics/plotting).

## Gradients

An objective has signature `objective(model, state, dt, step, forces)`. Use Julia
arithmetic and reductions inside Python objectives to preserve automatic
differentiation values; converting intermediates to `float` or NumPy loses
derivatives. The coupled state includes reservoir and wells, whereas
`result.states` contains only reservoir states.

With `output_substates=True`, `result.states` and `result.time` also include
internal solver steps. Pass the full result to `evaluate_objective` so its time
integration matches the adjoint.

Use `mode="default", output_substates=True` when reusing a forward result for
`reservoir_sensitivities`. `convert=True` returns a dictionary of NumPy gradients,
including `"porosity"` and `"permeability"`. The
[gradient example](examples/gradients.md) demonstrates the complete workflow.

`optimization_config` and `setup_reservoir_parameter_optimization` expose Julia
optimization callbacks; access `F!` with `getattr(problem, "F!")`. See the
[Julia adjoint guide](https://sintefmath.github.io/JutulDarcy.jl/stable/man/basics/adjoints)
for objectives, scaling and optimization algorithms.

## Upgrading from 1.2

- Python 3.10 and Julia 1.11 or newer are required. JuliaPkg now selects the
  registered JutulDarcy 0.4 series, Jutul 0.5 and MultiComponentFlash 2.
- Simulations default to KernelAbstractions on the CPU. Pass `mode="default"`
  to use the traditional simulator, including for adjoint workflows.
- Plotting returns a figure immediately. Scripts that should wait for a window
  to close must pass `block=True`. Backend loading errors retain their Julia
  diagnostics; install the backend before activating it.
- Numerical input arrays are copied into Julia. Rebuild or update the Julia
  model explicitly after changing Python input arrays.

## Configure Julia

Set configuration **before** importing `jutuldarcy` or `juliacall`:

```python
import os

os.environ["PYTHON_JULIAPKG_EXE"] = "/absolute/path/to/julia"  # Optional
os.environ["PYTHON_JULIACALL_THREADS"] = "4"
import jutuldarcy as jd
```

`PYTHON_JULIAPKG_PROJECT` selects a Julia project by absolute directory path;
JuliaPkg manages dependencies there. Import `jutuldarcy` first so it can enable
Julia's signal handling. See
[JuliaCall configuration](https://juliapy.github.io/PythonCall.jl/stable/juliacall/#Configuration).
