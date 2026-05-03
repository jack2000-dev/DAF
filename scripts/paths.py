"""Path helper for DAF projects.

Resolves the project root by walking up from this file until it finds
`pyproject.toml`, then exposes constants and helpers for every standard
subdirectory.

Why use this:
    - No more `../../data/raw/file.csv` strings.
    - Notebook works whether opened from `notebooks/`, `scripts/`, or root.
    - Output dirs auto-created on write.

Notebook setup (one-time, top cell):
    import sys
    from pathlib import Path
    ROOT = next(p for p in Path.cwd().resolve().parents if (p / "pyproject.toml").exists())
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

Usage:
    from scripts.paths import PATHS, raw, processed, report, visual, query

    df = pd.read_csv(raw("customers.csv"))
    df.to_parquet(processed("customers_clean.parquet"))
    fig.savefig(visual("churn_by_region.png"), dpi=150)
    sql = query("final/100_churn_summary.sql").read_text()
    print(PATHS)  # show resolved paths
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

_ROOT_MARKER = "pyproject.toml"


def _find_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / _ROOT_MARKER).exists():
            return parent
    raise RuntimeError(
        f"Project root not found from {start}. "
        f"Expected {_ROOT_MARKER} in an ancestor directory."
    )


ROOT: Path = _find_root(Path(__file__).resolve().parent)


class _Paths:
    """Namespace of project directories. All values are absolute Path objects."""

    root = ROOT

    data = ROOT / "data"
    raw = ROOT / "data" / "raw"
    processed = ROOT / "data" / "processed"
    external = ROOT / "data" / "external"

    docs = ROOT / "docs"
    notebooks = ROOT / "notebooks"

    queries = ROOT / "queries"
    queries_exploratory = ROOT / "queries" / "exploratory"
    queries_transformations = ROOT / "queries" / "transformations"
    queries_final = ROOT / "queries" / "final"

    reports = ROOT / "reports"
    scripts = ROOT / "scripts"
    visuals = ROOT / "visuals"

    def __repr__(self) -> str:
        keys = [k for k in vars(type(self)) if not k.startswith("_")]
        lines = [f"  {k:24s} {getattr(self, k)}" for k in keys]
        return "Paths(\n" + "\n".join(lines) + "\n)"


PATHS = _Paths()


def _join(base: Path, *parts: PathLike, mkdir: bool = False) -> Path:
    p = base.joinpath(*map(str, parts)) if parts else base
    if mkdir:
        target = p if p.suffix == "" else p.parent
        target.mkdir(parents=True, exist_ok=True)
    return p


def raw(*parts: PathLike) -> Path:
    return _join(PATHS.raw, *parts)


def processed(*parts: PathLike, mkdir: bool = True) -> Path:
    return _join(PATHS.processed, *parts, mkdir=mkdir)


def external(*parts: PathLike) -> Path:
    return _join(PATHS.external, *parts)


def notebook(*parts: PathLike) -> Path:
    return _join(PATHS.notebooks, *parts)


def query(*parts: PathLike) -> Path:
    return _join(PATHS.queries, *parts)


def report(*parts: PathLike, mkdir: bool = True) -> Path:
    return _join(PATHS.reports, *parts, mkdir=mkdir)


def visual(*parts: PathLike, mkdir: bool = True) -> Path:
    return _join(PATHS.visuals, *parts, mkdir=mkdir)


def doc(*parts: PathLike) -> Path:
    return _join(PATHS.docs, *parts)


def ensure_dirs() -> None:
    """Create all standard output directories if missing."""
    for d in (
        PATHS.raw,
        PATHS.processed,
        PATHS.external,
        PATHS.reports,
        PATHS.visuals,
        PATHS.notebooks,
    ):
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    print(PATHS)
