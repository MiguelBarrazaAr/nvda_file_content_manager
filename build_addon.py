from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path

import buildVars


EXCLUDED_DIRS = {"__pycache__", ".git", "build"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".db", ".sqlite", ".sqlite3", ".log", ".tmp"}


def build(project_dir: Path, output_dir: Path) -> Path:
	addon_info = buildVars.addon_info
	addon_name = addon_info["addon_name"]
	version = addon_info["addon_version"]
	build_root = output_dir / "staging"
	package_path = output_dir / f"{addon_name}-{version}.nvda-addon"

	if build_root.exists():
		shutil.rmtree(build_root)
	output_dir.mkdir(parents=True, exist_ok=True)
	shutil.copytree(
		project_dir / "addon",
		build_root,
		ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", "*.db", "*.sqlite", "*.sqlite3", "*.log", "*.tmp"),
	)
	_generate_manifest(project_dir / "manifest.ini.tpl", build_root / "manifest.ini", addon_info)

	if package_path.exists():
		package_path.unlink()
	with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
		for path in build_root.rglob("*"):
			if path.is_file() and _should_include(path, build_root):
				archive.write(path, path.relative_to(build_root).as_posix())
	shutil.rmtree(build_root)
	return package_path


def _generate_manifest(template_path: Path, destination: Path, addon_info: dict[str, str]) -> None:
	template = template_path.read_text(encoding="utf-8")
	destination.write_text(template.format(**addon_info), encoding="utf-8")


def _should_include(path: Path, root: Path) -> bool:
	relative = path.relative_to(root)
	if any(part in EXCLUDED_DIRS for part in relative.parts):
		return False
	if path.suffix.lower() in EXCLUDED_SUFFIXES:
		return False
	return True


def main() -> None:
	parser = argparse.ArgumentParser(description="Construir paquete .nvda-addon.")
	parser.add_argument("--project-dir", default=".")
	parser.add_argument("--output-dir", default="build")
	args = parser.parse_args()
	package_path = build(Path(args.project_dir).resolve(), Path(args.output_dir).resolve())
	print(package_path)


if __name__ == "__main__":
	main()

