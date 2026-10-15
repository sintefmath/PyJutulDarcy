Installation and Julia environment
==================================

Install the Python package in a virtual environment:

.. code-block:: bash

   python -m pip install jutuldarcy

The first ``import jutuldarcy`` uses
`JuliaPkg <https://github.com/JuliaPy/pyjuliapkg>`_ to locate or install Julia and
resolve the Julia dependencies declared in ``jutuldarcy/juliapkg.json``. The
initial installation needs network access and can take several minutes. Later
imports reuse the environment.

Source installations
--------------------

To work from a checkout:

.. code-block:: bash

   git clone https://github.com/sintefmath/PyJutulDarcy.git
   cd PyJutulDarcy
   python -m venv .venv
   # Activate .venv using your shell's activation command.
   python -m pip install -e .

The development dependencies select JutulDarcy 0.4 and Julia 1.11 or newer.
``Project.toml`` uses a Julia ``[sources]`` entry for JutulDarcy's development
source; ``juliapkg.json`` declares the same source for managed Python
environments. The source revision and compatible versions are defined in those
files.

Using an existing Julia installation
------------------------------------

Set configuration before the first import of either ``jutuldarcy`` or
``juliacall``:

.. code-block:: python

   import os

   os.environ["PYTHON_JULIAPKG_EXE"] = "/absolute/path/to/julia"
   os.environ["PYTHON_JULIACALL_THREADS"] = "4"
   import jutuldarcy as jd

To use a specific Julia project, set ``PYTHON_JULIAPKG_PROJECT`` to its absolute
directory path. Point it at the repository root to use the checked-in
``Project.toml``. JuliaPkg manages dependencies in the selected project.

The wrapper enables Julia signal handling before loading JuliaCall. Import
``jutuldarcy`` first when possible, so it can apply its runtime settings.
See `JuliaCall configuration
<https://juliapy.github.io/PythonCall.jl/stable/juliacall/#Configuration>`_
for the complete set of runtime options.
