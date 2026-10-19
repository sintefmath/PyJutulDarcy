"""Execute example sources and publish their code, output and saved figures."""

from contextlib import redirect_stdout
from io import StringIO
import logging
from pathlib import Path
import runpy
import sys
from tempfile import TemporaryDirectory

import matplotlib
import mkdocs_gen_files

matplotlib.use("Agg")
ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
log = logging.getLogger("mkdocs.examples")
sys.path.insert(0, str(EXAMPLES))
try:
    for source in sorted(EXAMPLES.glob("*.py")):
        log.info("Executing %s", source.name)
        example = runpy.run_path(str(source))
        captured = StringIO()
        with TemporaryDirectory(prefix=f"pyjutul-{source.stem}-") as directory:
            with redirect_stdout(captured):
                example["main"](output_dir=Path(directory))
            page = f"examples/{source.stem}.md"
            with mkdocs_gen_files.open(page, "w") as stream:
                description = example.get("__doc__", source.stem).strip()
                title, _, body = description.partition("\n")
                stream.write(f"# {title}\n\n{body.strip()}\n\n")
                stream.write("This example is executed during every documentation build.\n\n")
                stream.write(f"```python\n{source.read_text().rstrip()}\n```\n\n")
                output = captured.getvalue().strip()
                if output:
                    stream.write(f"## Output\n\n```text\n{output}\n```\n\n")
                for figure in sorted(Path(directory).glob("*.png")):
                    target = f"examples/{source.stem}/{figure.name}"
                    with mkdocs_gen_files.open(target, "wb") as image:
                        image.write(figure.read_bytes())
                    stream.write(f"![{figure.stem}]({source.stem}/{figure.name})\n\n")
            mkdocs_gen_files.set_edit_path(page, Path("..") / source.relative_to(ROOT))
finally:
    sys.path.pop(0)
