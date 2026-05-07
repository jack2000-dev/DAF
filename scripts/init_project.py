"""One-shot project initializer for the DAF template.

Run via `make init` immediately after cloning the template. Prompts for
project identity, rewrites template files in place, then self-destructs
(removes MANUAL.md, this script, and the `init` Makefile target).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _detect_python() -> str:
    v = sys.version_info
    return f"{v.major}.{v.minor}.{v.micro}"


def _detect_git_user() -> str:
    return _run(["git", "config", "user.name"])


def _detect_dir_name() -> str:
    return ROOT.name


def _ask(label: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    return answer or default


def _slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "project"


def _python_floor(version: str) -> str:
    parts = version.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version


def _rewrite_pyproject(name: str, description: str, py_floor: str) -> None:
    path = ROOT / "pyproject.toml"
    text = path.read_text()
    text = re.sub(r'^name\s*=\s*".*"', f'name = "{name}"', text, count=1, flags=re.M)
    text = re.sub(
        r'^description\s*=\s*".*"',
        f'description = "{description}"',
        text,
        count=1,
        flags=re.M,
    )
    text = re.sub(
        r'^requires-python\s*=\s*".*"',
        f'requires-python = ">={py_floor}"',
        text,
        count=1,
        flags=re.M,
    )
    path.write_text(text)


def _rewrite_python_version(version: str) -> None:
    (ROOT / ".python-version").write_text(version + "\n")


def _rewrite_readme(name: str, author: str) -> None:
    path = ROOT / "README.md"
    text = path.read_text()
    text = text.replace("[Project Title]", name, 1)
    if author:
        text = re.sub(
            r"\*Author:\s*\*\*[^*]+\*\*",
            f"*Author: **{author}**",
            text,
            count=1,
        )
    path.write_text(text)


def _rewrite_makefile(name: str) -> None:
    path = ROOT / "Makefile"
    text = path.read_text()
    text = text.replace('@echo "DAF commands:"', f'@echo "{name} commands:"', 1)
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    skip = False
    for line in lines:
        if line.startswith(".PHONY:"):
            line = line.replace(" init", "")
        if line.startswith("init:"):
            skip = True
            continue
        if skip:
            if line.strip() == "":
                skip = False
            continue
        if "make init" in line:
            continue
        out.append(line)
    path.write_text("".join(out))


def _self_destruct() -> None:
    manual = ROOT / "MANUAL.md"
    if manual.exists():
        manual.unlink()
    Path(__file__).unlink()


def main() -> int:
    if not (ROOT / "MANUAL.md").exists():
        print("Already initialized (MANUAL.md missing). Aborting.")
        return 1

    print("Initializing project from DAF template.\n")

    default_name = _slugify(_detect_dir_name())
    default_py = _detect_python()
    default_author = _detect_git_user()

    name = _slugify(_ask("Project name", default_name))
    description = _ask("Description", "Data analysis project")
    py_version = _ask("Python version", default_py)
    author = _ask("Author", default_author)

    py_floor = _python_floor(py_version)

    _rewrite_pyproject(name, description, py_floor)
    _rewrite_python_version(py_version)
    _rewrite_readme(name, author)
    _rewrite_makefile(name)
    _self_destruct()

    print(f"\n✓ Initialized {name} (Python {py_version})")
    print("  Next: uv sync && uv add pandas pyarrow jupyterlab")
    return 0


if __name__ == "__main__":
    sys.exit(main())
