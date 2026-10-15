Gradients and optimization
==========================

``reservoir_sensitivities`` accepts a Python callable or a Julia objective.
The objective receives ``(model, state, dt, step, forces)`` and its value is summed
over simulation steps. A coupled model's objective state includes the reservoir
and wells; ``result.states``, used for plotting, contains reservoir states only.

.. code-block:: python

   import jutuldarcy as jd

   def objective(model, state, dt, step, forces):
       pressure = state[jd.jl.Symbol("Reservoir")][jd.jl.Symbol("Pressure")]
       return jd.jl.sum(pressure) * dt

   result = jd.simulate_reservoir(case, mode="default", output_substates=True)
   gradients = jd.reservoir_sensitivities(case, result, objective, convert=True)

The adjoint uses the host model. Use the CPU path above when reusing a forward
result, and retain substates for timesteps that require multiple internal steps.
Alternatively, let the sensitivity helper perform the forward solve:

.. code-block:: python

   result, gradients = jd.reservoir_sensitivities(case, objective, convert=True)
   value = jd.evaluate_objective(objective, case, result)

``convert=True`` returns a dictionary whose entries, such as ``"porosity"`` and
``"permeability"``, are NumPy arrays. Without conversion, the gradient is a Julia
``DataDomain``. Lower-level parameter adjoints are available through
``solve_adjoint_sensitivities``.

Preserving automatic differentiation
------------------------------------

Python objectives receive Julia automatic-differentiation values. Use Julia
arithmetic and reductions, as above. Casting intermediate values to ``float`` or
NumPy can discard derivatives. A Julia function can also be supplied directly:

.. code-block:: python

   objective = jd.jl.seval(
       "(model, state, dt, step, forces) -> sum(state[:Reservoir][:Pressure])*dt"
   )

Optimization callbacks
----------------------

``optimization_config`` and ``setup_reservoir_parameter_optimization`` expose
Julia's optimization setup. Access callback names containing ``!`` with
``getattr``:

.. code-block:: python

   config = jd.optimization_config(case)
   problem = jd.setup_reservoir_parameter_optimization(case, objective, config)
   value = getattr(problem, "F!")(problem.x0)

``npv_objective``, ``setup_reservoir_dict_optimization`` and
``parameters_gradient_reservoir`` are also wrapped. Refer to the
`JutulDarcy documentation <https://sintefmath.github.io/JutulDarcy.jl/dev/>`_
for objective definitions, parameter scaling and optimization algorithms.
