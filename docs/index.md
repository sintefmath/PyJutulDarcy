# Reservoir simulation from Python

PyJutulDarcy wraps **JutulDarcy 0.4**, a differentiable multiphase reservoir
simulator. Run industry DATA files or build a model with Python and NumPy;
Julia performs the simulation and adjoint calculations.

## Install

```sh
python -m pip install jutuldarcy
```

The first `import jutuldarcy` installs Julia 1.11 or newer and the registered
Julia dependencies automatically. Allow several minutes and network access for
this step. Later imports reuse the installation; the first simulation also
compiles code for your model.

## Run a DATA file

```python
import jutuldarcy as jd

output = jd.simulate_data_file("MODEL.DATA", convert=True)
pressure = output["STATES"][-1]["Pressure"]  # NumPy array, Pa
days = output["DAYS"]
```

Start with the executed [SPE9 example](examples/spe9.md) to try a public dataset,
or [build a model from scratch](examples/standalone.md). The [user guide](guide.md)
explains indexing, results, backends and plotting; the [API reference](reference.md)
lists the Python entry points.

## Learn more in the Julia documentation

The Python interface exposes a subset of the full simulator. Use the
[Julia manual](https://sintefmath.github.io/JutulDarcy.jl/stable/) for the physics
and complete keyword options:

- [First model](https://sintefmath.github.io/JutulDarcy.jl/stable/man/first_ex)
  and [high-level API](https://sintefmath.github.io/JutulDarcy.jl/stable/man/highlevel/).
- [Input formats](https://sintefmath.github.io/JutulDarcy.jl/stable/man/basics/input_files)
  and [supported physical systems](https://sintefmath.github.io/JutulDarcy.jl/stable/man/basics/systems).
- [Examples](https://sintefmath.github.io/JutulDarcy.jl/stable/examples/overview/example_overview),
  covering CO₂ storage, geothermal, compositional flow and history matching.

For scientific use, cite the
[JutulDarcy paper](https://doi.org/10.1007/s10596-025-10366-6).
