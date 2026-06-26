# File Content Manager

Complemento global de NVDA para gestionar contenido de archivos de texto desde el Explorador de Windows.

## Estado

- Version: 2.0.0
- Compatibilidad minima: NVDA 2026.1
- Ultima version probada declarada: NVDA 2026.1
- Idioma base: espanol

## Funciones

- Copiar el contenido completo del archivo enfocado.
- Agregar el contenido de un archivo al texto ya existente en el portapapeles.
- Sobrescribir un archivo con el texto del portapapeles.
- Agregar el texto del portapapeles al final de un archivo.
- Ver el contenido de un archivo o del portapapeles en el visor navegable de NVDA.
- Escribir texto en un cuadro simple para copiarlo o agregarlo al portapapeles.
- Copiar rutas en formato Windows o con barras inclinadas.
- Crear un archivo en la carpeta actual usando el contenido del portapapeles.
- Abrir una ruta tomada desde el portapapeles.

## Atajos

Todos los comandos usan `scriptHandler.script`, tienen descripcion y quedan disponibles para reasignar desde NVDA > Preferencias > Gestos de entrada. En esa lista aparecen en una sola categoria, `File Content Manager`, con descripciones prefijadas por grupo: `Archivos:`, `Portapapeles:` y `Rutas:`.

| Atajo | Accion |
| --- | --- |
| NVDA+control+shift+c | Archivos: copia el contenido del archivo enfocado. |
| NVDA+control+alt+c | Archivos: agrega el contenido del archivo enfocado al portapapeles. |
| NVDA+control+shift+v | Archivos: sobrescribe el archivo enfocado con el portapapeles. |
| NVDA+control+alt+v | Archivos: agrega el portapapeles al final del archivo enfocado. |
| NVDA+shift+espacio | Archivos: muestra el contenido del archivo enfocado. |
| NVDA+control+shift+f | Archivos: crea un archivo en la carpeta actual con el contenido del portapapeles. |
| NVDA+alt+a | Portapapeles: abre un dialogo para escribir texto y copiarlo al portapapeles. |
| NVDA+control+shift+a | Portapapeles: abre un dialogo para escribir texto y agregarlo al portapapeles. |
| NVDA+control+shift+z | Portapapeles: muestra el texto del portapapeles. |
| NVDA+control+shift+r | Rutas: copia la ruta del elemento enfocado. |
| NVDA+control+alt+r | Rutas: copia la ruta con barras inclinadas. |
| NVDA+control+shift+d | Rutas: abre la ruta guardada en el portapapeles. |

## Estructura

```text
addon/
  globalPlugins/fileContentManager/
    __init__.py
    explorer.py
    text_ops.py
    version.py
  doc/es/readme.md
buildVars.py
build_addon.py
manifest.ini.tpl
```

## Build

Desde esta carpeta:

```powershell
python build_addon.py
```

El paquete queda en `build/fileContentManager-2.0.0.nvda-addon`.

## Notas de compatibilidad

Validado contra documentacion de NVDA 2026.1.1. El complemento usa `scriptHandler.script`, `ui.browseableMessage`, `gui.runScriptModalDialog` y acceso COM de Windows Shell para resolver el elemento enfocado en Explorer.

El complemento trabaja con archivos de texto UTF-8. Si un archivo usa otra codificacion, NVDA informa que no pudo decodificarlo.
