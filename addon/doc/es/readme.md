# File Content Manager

File Content Manager permite copiar, ver y escribir contenido de archivos de texto desde el Explorador de Windows usando comandos de NVDA.

## Compatibilidad

- Minimo: NVDA 2026.1
- Ultima version probada: NVDA 2026.1

## Comandos

Todos los comandos estan disponibles para reasignar desde NVDA > Preferencias > Gestos de entrada. Aparecen en una sola categoria, File Content Manager, con descripciones prefijadas por grupo: Archivos, Portapapeles y Rutas.

| Atajo | Accion |
| --- | --- |
| NVDA+control+shift+c | Archivos: copia el contenido del archivo enfocado. |
| NVDA+control+alt+c | Archivos: agrega el contenido del archivo al portapapeles. |
| NVDA+control+shift+v | Archivos: sobrescribe el archivo con el portapapeles. |
| NVDA+control+alt+v | Archivos: agrega el portapapeles al final del archivo. |
| NVDA+shift+espacio | Archivos: muestra el contenido del archivo. |
| NVDA+control+shift+f | Archivos: crea un archivo en la carpeta actual con el contenido del portapapeles. |
| NVDA+alt+a | Portapapeles: abre un dialogo para escribir texto y copiarlo al portapapeles. |
| NVDA+control+shift+a | Portapapeles: abre un dialogo para escribir texto y agregarlo al portapapeles. |
| NVDA+control+shift+z | Portapapeles: muestra el texto del portapapeles. |
| NVDA+control+shift+r | Rutas: copia la ruta del elemento enfocado. |
| NVDA+control+alt+r | Rutas: copia la ruta con barras inclinadas. |
| NVDA+control+shift+d | Rutas: abre la ruta del portapapeles. |

## Limitaciones

Las operaciones de lectura y escritura usan UTF-8. Si el archivo esta en otra codificacion, el complemento no lo modifica y muestra un mensaje de error.
