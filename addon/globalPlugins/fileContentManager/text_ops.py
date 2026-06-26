from __future__ import annotations

from pathlib import Path


TEXT_ENCODING = "utf-8"


class FileContentError(Exception):
	"""Base para errores controlados del complemento."""


class NotAFileError(FileContentError):
	pass


class EmptyClipboardError(FileContentError):
	pass


def read_text_file(path: str) -> str:
	file_path = _ensure_file(path)
	try:
		return file_path.read_text(encoding=TEXT_ENCODING)
	except PermissionError as exc:
		raise FileContentError("Permiso denegado al leer el archivo.") from exc
	except UnicodeDecodeError as exc:
		raise FileContentError("No se pudo decodificar el archivo como UTF-8.") from exc
	except OSError as exc:
		raise FileContentError(f"No se pudo leer el archivo: {exc}") from exc


def overwrite_text_file(path: str, text: str) -> None:
	file_path = _ensure_file(path)
	try:
		file_path.write_text(text, encoding=TEXT_ENCODING)
	except PermissionError as exc:
		raise FileContentError("Permiso denegado al escribir en el archivo.") from exc
	except OSError as exc:
		raise FileContentError(f"No se pudo escribir el archivo: {exc}") from exc


def append_text_file(path: str, text: str) -> None:
	file_path = _ensure_file(path)
	try:
		prefix = "\n" if file_path.stat().st_size > 0 else ""
		with file_path.open("a", encoding=TEXT_ENCODING) as file_obj:
			file_obj.write(prefix + text)
	except PermissionError as exc:
		raise FileContentError("Permiso denegado al escribir en el archivo.") from exc
	except OSError as exc:
		raise FileContentError(f"No se pudo agregar texto al archivo: {exc}") from exc


def create_file_next_to_path(reference_path: str, file_name: str, text: str) -> Path:
	reference = Path(reference_path)
	folder = reference if reference.is_dir() else reference.parent
	new_path = folder / _sanitize_file_name(file_name)
	try:
		new_path.write_text(text, encoding=TEXT_ENCODING)
	except PermissionError as exc:
		raise FileContentError("Permiso denegado al crear el archivo.") from exc
	except OSError as exc:
		raise FileContentError(f"No se pudo crear el archivo: {exc}") from exc
	return new_path


def combine_with_newline(first: str, second: str) -> str:
	if first and second:
		return f"{first}\n{second}"
	return first or second


def require_clipboard_text(text: str | None) -> str:
	if text is None or text == "":
		raise EmptyClipboardError("No hay texto en el portapapeles.")
	return text


def _ensure_file(path: str) -> Path:
	file_path = Path(path)
	if not file_path.is_file():
		raise NotAFileError("El elemento enfocado no es un archivo.")
	return file_path


def _sanitize_file_name(file_name: str) -> str:
	name = file_name.strip() or "a.txt"
	if any(separator in name for separator in ("\\", "/")):
		raise FileContentError("El nombre no debe incluir carpetas.")
	return name

