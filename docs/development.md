# Development

From a checkout, create and activate a Python virtual environment, then install:

```sh
python -m pip install -e '.[test,docs]'
```

`Project.toml` and `jutuldarcy/juliapkg.json` select registered JutulDarcy **0.4**
releases, without a Git checkout override. Keep their dependency constraints in
sync. Set `PYTHON_JULIAPKG_PROJECT` to the absolute repository path to use the
root Julia project, or leave it unset to test JuliaCall's managed environment.

## Checks

```sh
ruff check jutuldarcy tests examples docs/gen_examples.py
python -m pytest -m 'not plotting' -v
python -m build
```

Tests run real Julia simulations, DATA parsing and adjoints checked against
finite differences. GPU lifecycle tests use mocks and do not need GPU hardware.
To include the headless rendering test:

```sh
python -c "import jutuldarcy as jd; jd.install_plotting('CairoMakie')"
PYJUTULDARCY_TEST_PLOTTING=1 python -m pytest -v
```

## Documentation

```sh
python -c "import jutuldarcy as jd; jd.install_plotting('CairoMakie')"
python -m mkdocs build --strict
python -m mkdocs serve
```

Every build **executes all scripts in `examples/`**, including the SPE9 benchmark
(downloaded on first use), headless Makie rendering and adjoint gradients. Their
source, captured output and figures become the example pages. A failed example
fails the build; there is no skipped-execution mode. The API is collected
statically from the Python sources with mkdocstrings.

Keep example scripts importable and provide `main(output_dir=None)`. When an
output directory is supplied, save figures there without opening windows.
The documentation generator discovers scripts automatically. Add each new page
to `mkdocs.yml` so it appears in navigation.

CI builds the docs on pushes and pull requests; pushes to `main` also deploy
`site/` to GitHub Pages. The test matrix covers Linux and Windows, Python
3.10, 3.12 and 3.13, and Julia 1.11/1.12.
