from .julia_import import jl
from .conversion import _convert_units, convert_to_pydict

def simulate_data_file(data_file_name, convert = False, units = jl.missing, **kwargs):
    """
    Simulate a reservoir .DATA file using JutulDarcy and return the results as a
    Python dictionary. The resulting dictionary has the following fields:

    - WELLS: A dictionary of well results, where each key is a well name and the
      value is a dictionary of results for that well.
    - FIELD: A dictionary of field results.
    - DAYS: A numpy array of time in days.
    - STATES: A list of dictionaries, each representing the state of the reservoir
      at a given time step. The field vary based on the type of simulation.
    
    If you are looking for files to test, see test_file_path() for a few
    examples of files to test.

    Examples:
    pth = test_file_path("SPE1", "SPE1.DATA")
    # Simulate the data file and convert to Python dictionary
    res = jd.simulate_data_file(pth, units = "field", restart = True, output_path = "/tmp")
    # Write output to disk and apply restart (restarting if simulation was aborted, otherwise retrieving results from disk)
    import tempfile
    res = jd.simulate_data_file(pth, restart = True, output_path = tempfile.gettempdir())
    # Simulate and change the units to field units even if input file has other units
    res = jd.simulate_data_file(pth, units = "field")

    """
    units = _convert_units(units)
    res = jl.JutulDarcy.simulate_data_file(data_file_name, **kwargs)
    if convert:
        out = convert_to_pydict(res, units=units)
    else:
        out = res
    return out

def simulate_reservoir(*arg, convert = False, units = jl.missing, **kwargs):
    """
    Simulate a reservoir using JutulDarcy and return the results as a Python
    dictionary. The resulting dictionary has the following fields:

    - WELLS: A dictionary of well results, where each key is a well name and the
      value is a dictionary of results for that well.
    - FIELD: A dictionary of field results.
    - DAYS: A numpy array of time in days.
    - STATES: A list of dictionaries, each representing the state of the reservoir
      at a given time step. The field vary based on the type of simulation.

    Examples:
    res = jd.simulate_reservoir(...)
    """
    res = jl.JutulDarcy.simulate_reservoir(*arg, **kwargs)
    if convert:
        out = convert_to_pydict(res, units=units)
    else:
        out = res
    return out

