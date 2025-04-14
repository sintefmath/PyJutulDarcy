from .julia_import import jl

def setup_case_from_data_file(*arg, **kwargs):
    """
    Setup a JutulDarcy case from a .DATA file. This function is used to set up a
    case for simulation. It does not run the simulation itself.

    Examples:
    case = jd.setup_case_from_data_file(filename, <kwargs>)
    """
    res = jl.JutulDarcy.setup_case_from_data_file(*arg, **kwargs)
    return res

def parse_data_file(data_file_name, **kwargs):
    """
    Parse a .DATA file and return the parsed data as a Julia dictionary.
    Examples:
    pth = test_file_path("SPE1", "SPE1.DATA")
    res = jd.parse_data_file(pth)
    """
    res = jl.GeoEnergyIO.parse_data_file(data_file_name, **kwargs)
    return res

def test_file_path(*args):
    """
    Get the path to a test file in the GeoEnergyIO package. This may trigger a
    download if it is the first time the given example file is requested. If a
    path is returned, the file is available on-disk at that location.

    Examples:
    test_file_path("SPE1", "SPE1.DATA")
    test_file_path("SPE9", "SPE9.DATA")
    test_file_path("OLYMPUS_1", "OLYMPUS_1.DATA")
    test_file_path("NORNE_NOHYST", "NORNE_NOHYST.DATA")
    test_file_path("EGG", "EGG.DATA")

    """
    return jl.GeoEnergyIO.test_input_file_path(*args)
