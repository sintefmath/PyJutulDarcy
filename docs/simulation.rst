Simulation and results
======================

Running a case
--------------

.. code-block:: python

   from pathlib import Path
   import jutuldarcy as jd

   case = jd.setup_case_from_data_file(Path("MODEL.DATA"))
   result = jd.simulate_reservoir(case)
   output = jd.convert_to_pydict(result, case, units="field")

``simulate_data_file(path, convert=True)`` combines case setup, simulation and
conversion. Cases built in Python use the same simulator interface; see the
repository's `standalone example
<https://github.com/sintefmath/PyJutulDarcy/blob/main/examples/standalone.py>`_.

Execution backends
------------------

``simulate_reservoir``, ``simulate_data_file`` and ``setup_reservoir_simulator``
default to ``mode="ka"``: KernelAbstractions on the CPU.

.. list-table::
   :header-rows: 1

   * - Selection
     - Execution
   * - ``mode="ka"`` or ``mode="ka_cpu"``
     - CPU kernels
   * - ``mode="ka_cpu_static"``
     - CPU kernels with static scheduling
   * - ``mode="default"``
     - Traditional CPU simulator
   * - ``gpu=True`` or ``mode="gpu"``
     - Activated, functional CUDA backend, then AMDGPU
   * - ``gpu="cuda"`` or ``mode="ka_cuda"``
     - Activated CUDA backend
   * - ``gpu="amd"`` or ``mode="ka_amd"``
     - Activated AMDGPU backend

Activate a GPU package before selecting it:

.. code-block:: python

   usable = jd.activate_cuda()  # Or jd.activate_amd().
   if usable:
       result = jd.simulate_reservoir(case, gpu=True)

Activation adds the Julia package only if it is absent, loads it and returns its
``functional()`` status. ``available_backends()`` lists activated, functional GPU
backends. Requesting an unavailable GPU raises an error.
``remove_cuda()`` and ``remove_amd()`` remove the corresponding requirement and
disable automatic selection. Restart Python to unload a loaded Julia module.

For custom KernelAbstractions devices, pass a Julia backend object as
``ka_backend`` with ``mode="ka"``. See the `upstream simulator documentation
<https://sintefmath.github.io/JutulDarcy.jl/dev/man/highlevel/>`_ for supported
model options and device limitations.

To reuse a simulator, select its mode when constructing it:

.. code-block:: python

   simulator, config = jd.setup_reservoir_simulator(case, mode="ka")
   result = jd.simulate_reservoir(case, simulator=simulator, config=config)

Python results
--------------

Simulation returns a Julia ``ReservoirSimResult`` unless ``convert=True`` is
requested. Converted results have these entries:

.. list-table::
   :header-rows: 1

   * - Entry
     - Python value
   * - ``FIELD``
     - Dictionary of field summary arrays
   * - ``WELLS``
     - Dictionary of well names, each containing summary arrays
   * - ``DAYS``
     - NumPy array of reporting times in days
   * - ``STATES``
     - List of reservoir state dictionaries with NumPy arrays

``units`` accepts ``"si"``, ``"metric"``, ``"field"`` or ``"lab"`` and controls
summary conversion. State arrays retain the simulation's units.
When calling ``convert_to_pydict`` separately, supply the case for results from
``simulate_reservoir``. Results from ``simulate_data_file`` retain their case.
