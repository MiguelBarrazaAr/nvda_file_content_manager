from __future__ import annotations

from pathlib import Path

import api
import controlTypes
from comtypes.client import CreateObject as COMCreate
from logHandler import log


EXPLORER_APP_NAMES = {"explorer", "cabinetwclass"}


def get_focused_explorer_path() -> str | None:
	focus = api.getFocusObject()
	foreground = api.getForegroundObject()
	if not focus and not foreground:
		return None
	if _app_name(focus) not in EXPLORER_APP_NAMES and _app_name(foreground) not in EXPLORER_APP_NAMES:
		return None

	shell = COMCreate("shell.application")
	window_handle = getattr(foreground, "windowHandle", None) or _window_handle(focus)
	for window in shell.Windows():
		try:
			if not _same_explorer_window(window, window_handle):
				continue
			path = _focused_item_path(window)
			if path:
				return path
			return _folder_path(window)
		except Exception:
			log.debugWarning("No se pudo resolver el elemento enfocado en Explorer.", exc_info=True)
	return None


def path_for_display(path: str) -> str:
	return str(Path(path))


def path_with_forward_slashes(path: str) -> str:
	return path.replace("\\", "/")


def _app_name(obj) -> str:
	try:
		return obj.appModule.appName.lower()
	except Exception:
		return ""


def _window_handle(obj) -> int | None:
	current = obj
	while current:
		handle = getattr(current, "windowHandle", None)
		role = getattr(current, "role", None)
		if handle and role in (controlTypes.Role.PANE, controlTypes.Role.WINDOW):
			return handle
		current = getattr(current, "parent", None)
	return getattr(obj, "windowHandle", None)


def _same_explorer_window(window, window_handle: int | None) -> bool:
	if not window_handle:
		return False
	return bool(getattr(window, "hwnd", None)) and int(window.hwnd) == int(window_handle)


def _focused_item_path(window) -> str | None:
	item = window.Document.FocusedItem
	if not item:
		return None
	path = getattr(item, "Path", None) or getattr(item, "path", None)
	return str(path) if path else None


def _folder_path(window) -> str | None:
	folder = window.Document.Folder
	if not folder:
		return None
	path = getattr(folder.Self, "Path", None) or getattr(folder.Self, "path", None)
	return str(path) if path else None
