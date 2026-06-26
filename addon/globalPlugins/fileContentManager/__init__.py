# -*- coding: utf-8 -*-
from __future__ import annotations

import os

import api
import globalPluginHandler
import gui
import wx
from scriptHandler import script
from ui import browseableMessage, message

from .explorer import (
	get_focused_explorer_path,
	path_for_display,
	path_with_forward_slashes,
)
from .text_ops import (
	EmptyClipboardError,
	FileContentError,
	append_text_file,
	combine_with_newline,
	create_file_next_to_path,
	overwrite_text_file,
	read_text_file,
	require_clipboard_text,
)


CATEGORY = "File Content Manager"


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@script(
		gesture="kb:NVDA+control+shift+c",
		category=CATEGORY,
		description="Archivos: copia al portapapeles el contenido del archivo enfocado.",
	)
	def script_copyFocusedFileContent(self, gesture):
		path = self._focused_path(require_file=True)
		if not path:
			return
		try:
			api.copyToClip(read_text_file(path))
			message("Contenido copiado al portapapeles.")
		except FileContentError as exc:
			message(str(exc))

	@script(
		gesture="kb:NVDA+control+alt+c",
		category=CATEGORY,
		description="Archivos: agrega al portapapeles el contenido del archivo enfocado.",
	)
	def script_appendFocusedFileContentToClipboard(self, gesture):
		path = self._focused_path(require_file=True)
		if not path:
			return
		try:
			file_text = read_text_file(path)
			api.copyToClip(combine_with_newline(api.getClipData() or "", file_text))
			message("Contenido del archivo agregado al portapapeles.")
		except FileContentError as exc:
			message(str(exc))

	@script(
		gesture="kb:NVDA+control+shift+v",
		category=CATEGORY,
		description="Archivos: sobrescribe el archivo enfocado con el texto del portapapeles.",
	)
	def script_overwriteFocusedFileFromClipboard(self, gesture):
		path = self._focused_path(require_file=True)
		if not path:
			return
		try:
			overwrite_text_file(path, require_clipboard_text(api.getClipData()))
			message("Archivo sobrescrito con el portapapeles.")
		except (EmptyClipboardError, FileContentError) as exc:
			message(str(exc))

	@script(
		gesture="kb:NVDA+control+alt+v",
		category=CATEGORY,
		description="Archivos: agrega al final del archivo enfocado el texto del portapapeles.",
	)
	def script_appendClipboardToFocusedFile(self, gesture):
		path = self._focused_path(require_file=True)
		if not path:
			return
		try:
			append_text_file(path, require_clipboard_text(api.getClipData()))
			message("Portapapeles agregado al final del archivo.")
		except (EmptyClipboardError, FileContentError) as exc:
			message(str(exc))

	@script(
		gesture="kb:NVDA+shift+space",
		category=CATEGORY,
		description="Archivos: muestra en el visor el contenido del archivo enfocado.",
	)
	def script_showFocusedFileInViewer(self, gesture):
		path = self._focused_path(require_file=True)
		if not path:
			return
		try:
			browseableMessage(read_text_file(path), title="Contenido del archivo", isHtml=False)
		except FileContentError as exc:
			message(str(exc))

	@script(
		gesture="kb:NVDA+control+shift+f",
		category=CATEGORY,
		description="Archivos: crea un archivo en la carpeta actual con el contenido del portapapeles.",
	)
	def script_createFileFromClipboard(self, gesture):
		path = self._focused_path()
		if not path:
			return

		def create_file(file_name: str) -> None:
			try:
				new_path = create_file_next_to_path(path, file_name, api.getClipData() or "")
				message(f"Archivo creado: {new_path.name}")
			except FileContentError as exc:
				message(str(exc))

		self._show_text_dialog(
			title="Crear archivo",
			prompt="Nombre del nuevo archivo:",
			default_value="a.txt",
			on_accept=create_file,
		)

	@script(
		gesture="kb:NVDA+alt+a",
		category=CATEGORY,
		description="Portapapeles: abre un dialogo para escribir texto y copiarlo al portapapeles.",
	)
	def script_copyTypedTextToClipboard(self, gesture):
		self._show_text_dialog(
			title="Entrada de texto",
			prompt="Escribe el texto a copiar:",
			on_accept=lambda text: self._copy_text(text, "Texto copiado al portapapeles."),
		)

	@script(
		gesture="kb:NVDA+control+shift+a",
		category=CATEGORY,
		description="Portapapeles: abre un dialogo para escribir texto y agregarlo al portapapeles.",
	)
	def script_appendTypedTextToClipboard(self, gesture):
		def append_text(text: str) -> None:
			api.copyToClip(combine_with_newline(api.getClipData() or "", text))
			message("Texto agregado al portapapeles.")

		self._show_text_dialog(
			title="Entrada de texto",
			prompt="Escribe el texto a agregar:",
			on_accept=append_text,
		)

	@script(
		gesture="kb:NVDA+control+shift+z",
		category=CATEGORY,
		description="Portapapeles: muestra en el visor el texto del portapapeles.",
	)
	def script_showClipboardInViewer(self, gesture):
		try:
			content = require_clipboard_text(api.getClipData())
		except EmptyClipboardError as exc:
			message(str(exc))
			return
		browseableMessage(content, title="Texto del portapapeles", isHtml=False)

	@script(
		gesture="kb:NVDA+control+shift+r",
		category=CATEGORY,
		description="Rutas: copia al portapapeles la ruta del elemento enfocado.",
	)
	def script_copyFocusedPath(self, gesture):
		path = self._focused_path()
		if not path:
			return
		self._copy_text(path_for_display(path), "Ruta copiada al portapapeles.")

	@script(
		gesture="kb:NVDA+control+alt+r",
		category=CATEGORY,
		description="Rutas: copia la ruta del elemento enfocado usando barras inclinadas.",
	)
	def script_copyFocusedPathWithForwardSlashes(self, gesture):
		path = self._focused_path()
		if not path:
			return
		self._copy_text(path_with_forward_slashes(path), "Ruta con barras inclinadas copiada al portapapeles.")

	@script(
		gesture="kb:NVDA+control+shift+d",
		category=CATEGORY,
		description="Rutas: abre en Windows la ruta del portapapeles.",
	)
	def script_openPathFromClipboard(self, gesture):
		try:
			path = require_clipboard_text(api.getClipData()).replace("/", "\\")
			os.startfile(path)
			message("Ruta abierta.")
		except EmptyClipboardError as exc:
			message(str(exc))
		except OSError as exc:
			message(f"No se pudo abrir la ruta: {exc}")

	def _focused_path(self, require_file: bool = False) -> str | None:
		path = get_focused_explorer_path()
		if not path:
			message("No hay elemento enfocado en el Explorador de Windows.")
			return None
		if require_file and not os.path.isfile(path):
			message("El elemento enfocado no es un archivo.")
			return None
		return path

	def _show_text_dialog(self, title: str, prompt: str, on_accept, default_value: str = "") -> None:
		dialog = wx.TextEntryDialog(
			gui.mainFrame,
			prompt,
			title,
			default_value,
			style=wx.OK | wx.CANCEL,
		)

		def callback(result):
			if result == wx.ID_OK:
				on_accept(dialog.GetValue())
			dialog.Destroy()

		gui.runScriptModalDialog(dialog, callback)

	def _copy_text(self, text: str, confirmation: str) -> None:
		api.copyToClip(text)
		message(confirmation)
