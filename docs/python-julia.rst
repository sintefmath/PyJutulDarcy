Python and Julia values
=======================

Wrapped functions accept Python lists, tuples, dictionaries, NumPy arrays and
``pathlib.Path`` objects. The wrapper converts these to native Julia containers;
existing Julia objects pass through. Returned models, domains, cases and
simulators remain Julia objects.

Arrays and indexing
-------------------

Cell indices, well coordinates and region numbers passed to wrapper functions
follow **Julia's one-based convention**. Subscripting JuliaCall arrays from
Python, including ``result.states``, uses **zero-based Python indexing**, as do
NumPy outputs. Explicit Julia calls such as ``jd.jl.getindex(array, 1)`` use
Julia indexing.

Array shape is preserved. A per-cell, multiphase property is normally represented
as ``(number_of_phases, number_of_cells)``. Numerical inputs are copied into Julia
arrays; modifying the original NumPy array later does not update the model.

.. code-block:: python

   import jutuldarcy as jd
   import numpy as np

   mesh = jd.reservoir_mesh((3, 1, 1), (30.0, 10.0, 10.0))
   domain = jd.reservoir_domain(
       mesh, permeability=np.full(3, 1e-12), porosity=[0.2, 0.25, 0.3]
   )
   injector = jd.setup_well(domain, [1], name="Injector")
   producer = jd.setup_well(domain, (3, 1, 1), name="Producer")

Dictionaries and symbols
------------------------

Python dictionary keys become Julia ``Symbol`` keys by default, recursively.
This supports controls, limits, states and parameter dictionaries.
Use ``to_julia(data, symbols=False)`` when string keys must be retained, as in
parsed DATA/GRDECL dictionaries. Parsing and reservoir-grid wrappers already
handle this distinction.

.. code-block:: python

   state = jd.to_julia({"Pressure": [1e7, 1e7, 1e7]})
   pressure = state[jd.jl.Symbol("Pressure")]
   python_state = jd.to_python(state)  # dict with NumPy arrays

String options representing Julia symbols, such as well names, simulator
``mode`` and model ``backend``, are converted by their wrapper functions.
Direct Julia calls require explicit conversions where needed.

Using the Julia API directly
----------------------------

The loaded modules are available as ``jd.jl.JutulDarcy``, ``jd.jl.Jutul``,
``jd.jl.GeoEnergyIO`` and ``jd.jl.MultiComponentFlash``. This provides access to
functions that do not have a dedicated Python wrapper.

Julia mutators ending in ``!`` are accessed with ``getattr`` in Python. Wrapped
mutators drop the exclamation mark and return the modified model:

.. code-block:: python

   jd.set_relative_permeability(model, swof=table)
   # Direct equivalent after converting the table:
   getattr(jd.jl.JutulDarcy, "set_relative_permeability!")(
       model, swof=jd.to_julia(table)
   )

After replacing property definitions, recreate separately stored parameters
with ``jd.setup_parameters(model)`` before building a case.
See `JuliaCall's conversion guide
<https://juliapy.github.io/PythonCall.jl/stable/conversion-to-julia/>`_ for
conversions outside the wrapper.
