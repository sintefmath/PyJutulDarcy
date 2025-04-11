# PyJutulDarcy

Python wrapper for [JutulDarcy.jl, a fully differentiable reservoir simulator written in Julia](https://github.com/sintefmath/JutulDarcy.jl). This package facilitates automatic installation of JutulDarcy from Python, as well as a minimal interface that allows fast simulation of .DATA files in pure Python.

The package also provides access to all the functions of the Julia version under `jutuldarcy.jl.JutulDarcy`, `jutuldarcy.jl.GeoEnergyIO` and `jutuldarcy.jl.Jutul`. These functions are directly wrapped using [JuliaCall](https://github.com/JuliaPy/PythonCall.jl). For more details, see the [JuliaCall Documentation on converting of types](https://juliapy.github.io/PythonCall.jl/stable/conversion-to-julia/).

## Installation

The package can be installed with pip:

```julia
pip install jutuldarcy
```

On first time usage of the package [JuliaCall](https://github.com/JuliaPy/PythonCall.jl) will automatically install Julia and manage all dependency packages.

## A minimal example

```python
import jutuldarcy as jd
# Load SPE9 dataset to disk
pth = jd.test_file_path("SPE9", "SPE9.DATA")
# Simulate the model
res = jd.simulate_data_file(pth)
# Get field quantities and plot
import matplotlib.pyplot as plt
fopr = res["FIELD"]["FOPR"]
days = res["DAYS"]
plt.plot(days, fopr)
plt.ylabel("Field oil production")
plt.xlabel("Days")
plt.show()
```
<img width="299" alt="pyplot_fopr" src="https://github.com/user-attachments/assets/9b69bdee-91d9-4b37-ba20-05725f224cd9" />

Here, res is a standard dict containing the following fields:

- "FIELD": Field quantities (average pressure, total water injection, etc) as numpy arrays.
- "WELLS": Well quantities (bottom hole pressures, injection rates, production rates, etc)
- "STATES": Reservoir states for all active cells, given as a list with a dict for each timestep. For example, `res["STATES"][10]["Rs"]` will give you an array of the solution gas-oil-ratio at step 10.
- "DAYS": Array of the number of days elapsed for each step.

Optionally, `convert = False` can be passed to get access to the "full" output as seen in Julia, where it is possible to get access to grid geometry, model parameters, and so on.

## Paper and citing

The main paper describing `JutulDarcy.jl` is *JutulDarcy.jl - a Fully Differentiable High-Performance Reservoir Simulator Based on Automatic Differentiation*:

```bibtex
@article{jutuldarcy_ecmor_2024,
   author = "M{\o}yner, O.",
   title = "JutulDarcy.jl - a Fully Differentiable High-Performance Reservoir Simulator Based on Automatic Differentiation", 
   year = "2024",
   volume = "2024",
   number = "1",
   pages = "1-9",
   doi = "https://doi.org/10.3997/2214-4609.202437111",
   publisher = "European Association of Geoscientists \& Engineers",
   issn = "2214-4609",
}
```

## Contributing

Contributions that expose additional functionality is welcome.
