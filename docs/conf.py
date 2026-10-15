"""Build the Python wrapper reference without importing JuliaCall."""

from datetime import date
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "pyproject.toml").open("rb") as stream:
    metadata = tomllib.load(stream)["project"]

project = "PyJutulDarcy"
author = ", ".join(person["name"] for person in metadata["authors"])
copyright = f"{date.today().year}, {author}"
release = metadata["version"]

extensions = ["autoapi.extension", "sphinx.ext.napoleon", "sphinx.ext.githubpages"]
html_theme = "furo"
html_title = project
html_baseurl = "https://sintefmath.github.io/PyJutulDarcy/"
html_theme_options = {
    "source_repository": "https://github.com/sintefmath/PyJutulDarcy/",
    "source_branch": "main",
    "source_directory": "docs/",
}
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
nitpicky = True

# AutoAPI reads the Python source with static analysis. Importing this package
# during a documentation build would otherwise initialize Julia and its packages.
autoapi_dirs = [str(ROOT / "jutuldarcy")]
autoapi_root = "api"
autoapi_ignore = ["*/julia_import.py"]
# Runtime-only JuliaCall imports are intentionally outside the static reference.
# Keep all other documentation and cross-reference warnings fatal.
suppress_warnings = ["autoapi.python_import_resolution"]
autoapi_options = ["members", "undoc-members", "show-module-summary"]
autoapi_add_toctree_entry = False
autoapi_member_order = "bysource"
