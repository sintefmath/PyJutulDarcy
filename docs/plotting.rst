Plotting from Python
====================

Interactive plots
-----------------

Install and activate GLMakie once in the Python-managed Julia environment:

.. code-block:: python

   import jutuldarcy as jd

   jd.install_plotting()
   figure = jd.plot_reservoir(case.model, result)

GLMakie requires an OpenGL-capable display. Plotting returns a Makie figure
immediately and integrates Julia's event loop with the Python REPL or a running
``asyncio`` loop. In a script, use ``block=True`` to keep the window alive until it
is closed:

.. code-block:: python

   figure = jd.plot_reservoir(case.model, result, block=True)

The second argument may be a simulation result, native Julia states or a list of
Python state dictionaries. ``plot_well_results``, ``plot_reservoir_measurables``
and ``plot_summary`` expose the corresponding Julia plots. Plotting errors retain
their Julia diagnostics.

Headless rendering
------------------

CairoMakie supports saving static figures without a display:

.. code-block:: python

   jd.install_plotting("CairoMakie")
   figure = jd.plot_reservoir(case.model, result, display=False, key="Pressure")
   jd.jl.CairoMakie.save("pressure.png", figure)

The wrapper selects ``gui=False`` and ``force_glmakie=False`` for reservoir plots
when CairoMakie is active. Use ``key`` to choose the cell property to render.
``activate_plotting(backend)`` loads an already installed backend;
``uninstall_plotting(backend)`` removes its requirement. The default backend name
for these helpers is ``"GLMakie"``.
