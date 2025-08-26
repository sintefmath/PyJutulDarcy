import os
import sys
import warnings
# The following code that handles juliacall issues is copied from PySR
# Copyright 2020 Miles Cranmer, Apache 2.0 License.
# Source: https://github.com/MilesCranmer/PySR/blob/cd055a67728eeb675c76dedfe5d5e669eea3a6d1/pysr/julia_import.py

if "juliacall" in sys.modules:
    warnings.warn(
        "juliacall module already imported. "
        "Make sure that you have set the environment variable `PYTHON_JULIACALL_HANDLE_SIGNALS=yes` to avoid segfaults. "
        "Also note that jutuldarcy will not be able to configure `PYTHON_JULIACALL_THREADS` or `PYTHON_JULIACALL_OPTLEVEL` for you."
    )
else:
    # Required to avoid segfaults (https://juliapy.github.io/PythonCall.jl/dev/faq/)
    if os.environ.get("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes") != "yes":
        warnings.warn(
            "PYTHON_JULIACALL_HANDLE_SIGNALS environment variable is set to something other than 'yes' or ''. "
            + "You will experience segfaults if running with multithreading."
        )

    # TODO: Remove these when juliapkg lets you specify this
    for k, default in (
        ("PYTHON_JULIACALL_HANDLE_SIGNALS", "yes"),
        # ("PYTHON_JULIACALL_THREADS", "auto"),
        ("PYTHON_JULIACALL_OPTLEVEL", "3"),
    ):
        os.environ[k] = os.environ.get(k, default)


# Add packages to project
import juliapkg as jpkg

jpkg.add("JutulDarcy", "82210473-ab04-4dce-b31b-11573c4f8e0a", version="0.2")
jpkg.add("HYPRE", "b5ffcf37-a2bd-41ab-a3da-4bd9bc8ad771", version="1")
jpkg.add("Jutul", "2b460a1a-8a2b-45b2-b125-b5c536396eb9", version="0.3")
jpkg.add("GeoEnergyIO", "3b1dd628-313a-45bb-9d8d-8f3c48dcb5d4", version="1")
jpkg.add("MultiComponentFlash", "35e5bd01-9722-4017-9deb-64a5d32478ff", version="1")


# Actual start of module - now that juliacall can be imported
import juliacall
from juliacall import convert as jlconvert
jl = juliacall.newmodule("JutulDarcy")
import numpy as np

# Load the main package + linear solver
jl.seval("using JutulDarcy, Jutul, HYPRE, MultiComponentFlash, GeoEnergyIO")
jl.seval("import JutulDarcy: summary_result")
