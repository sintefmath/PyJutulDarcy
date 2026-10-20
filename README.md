# PyJutulDarcy

Python wrapper for [JutulDarcy.jl, a fully differentiable reservoir simulator written in Julia](https://github.com/sintefmath/JutulDarcy.jl). Key features:

- Immiscible, black-oil and compositional multiphase flow
- Geothermal simulation and simulation of CO2 sequestration
- Can read standard input files and corner-point grids, or make your own

This package facilitates automatic installation of JutulDarcy from Python, as well as a minimal interface that allows fast simulation of .DATA files in pure Python. For more details about JutulDarcy.jl, please see the [Julia Documentation](https://sintefmath.github.io/JutulDarcy.jl/stable/). If you want to run MPI accelerated simulations we recommend working either in Julia or the [standalone compiled version](https://github.com/sintefmath/JutulDarcyApps.jl).

For wrapper-specific installation, Python/Julia conversions and API reference, see the [Python documentation](https://sintefmath.github.io/PyJutulDarcy/).

The package also provides access to all the functions of the Julia version under `jutuldarcy.jl.JutulDarcy`, `jutuldarcy.jl.GeoEnergyIO` and `jutuldarcy.jl.Jutul`. These functions are directly wrapped using [JuliaCall](https://github.com/JuliaPy/PythonCall.jl). For more details, see the [JuliaCall Documentation on converting of types](https://juliapy.github.io/PythonCall.jl/stable/conversion-to-julia/).

## Installation

Requires Python 3.10 or newer.

```sh
python -m pip install jutuldarcy
```

The first import automatically installs Julia and the registered
**JutulDarcy** dependencies. Initial installation and compilation take several
minutes and need network access.

## Quick start

```python
import jutuldarcy as jd

path = jd.test_file_path("SPE9", "SPE9.DATA")
output = jd.simulate_data_file(path, convert=True)
pressure = output["STATES"][-1]["Pressure"]  # NumPy array in Pa
```

Converted results contain `FIELD` and `WELLS` summary dictionaries, a `DAYS` array
and one reservoir state dictionary per output time in `STATES`. Omit
`convert=True` to retain the native Julia result. Cell and well coordinates in
wrapper inputs are **one-based**; Python/NumPy array indexing is zero-based.

The [Python documentation](https://sintefmath.github.io/PyJutulDarcy/) includes
executed examples for [building a model](https://sintefmath.github.io/PyJutulDarcy/examples/standalone/),
[running SPE9](https://sintefmath.github.io/PyJutulDarcy/examples/spe9/),
[plotting](https://sintefmath.github.io/PyJutulDarcy/examples/plots/) and
[computing gradients](https://sintefmath.github.io/PyJutulDarcy/examples/gradients/). Every documentation build runs these
scripts and publishes their output and figures.

For interactive 3D plots, run `jd.install_plotting()` once (requires OpenGL).
For headless rendering, use `jd.install_plotting("CairoMakie")`. See the
[user guide](https://sintefmath.github.io/PyJutulDarcy/guide/) for results,
execution backends and Julia configuration, and the
[Julia manual](https://sintefmath.github.io/JutulDarcy.jl/stable/) for model physics
and the complete simulator API.

## Paper and citing

The main paper describing `JutulDarcy.jl` is [*JutulDarcy.jl - a Fully Differentiable High-Performance Reservoir Simulator Based on Automatic Differentiation*, available as open access from Springer](https://link.springer.com/article/10.1007/s10596-025-10366-6#citeas):

```bibtex
@article{jutuldarcy,
  title={JutulDarcy.jl - a fully differentiable high-performance reservoir simulator based on automatic differentiation},
  author={M{\o}yner, Olav},
  journal={Computational Geosciences},
  volume={29},
  number={30},
  year={2025},
  publisher={Springer}
}
```

## Contributing

Contributions that expose additional functionality is welcome. See the [contributor guide](https://sintefmath.github.io/PyJutulDarcy/development/) for tests and documentation builds.

## Releasing to PyPI

The [release workflow](.github/workflows/release.yml) publishes a wheel and source
distribution when a tag named `v<version>` is pushed. The tag must exactly match
`project.version` in `pyproject.toml`, for example `v1.2.2` for version `1.2.2`.
Prereleases use the same convention, for example `v1.3.0rc1`.

To release, update `project.version` in `pyproject.toml`, merge the change into
`main`, then create and push an annotated tag for that commit:

```sh
git switch main
git pull --ff-only
git tag -a v1.2.2 -m "Release 1.2.2"
git push origin v1.2.2
```

Use the version being released in place of `1.2.2`. After the workflow builds and
validates the distributions, review the tagged commit and approve the `pypi`
environment deployment. Publishing uses short-lived OIDC credentials and creates
PyPI attestations; no PyPI API token or GitHub secret is needed. The publishing
job only downloads the artifacts built in the same workflow run and uploads them
to PyPI. Action dependencies are pinned to commit SHAs, and Dependabot proposes
updates monthly.

Each PyPI version can only be published once. If a release fails partway through
uploading, inspect the files already on PyPI before retrying; the workflow fails
on existing files rather than silently skipping them.
