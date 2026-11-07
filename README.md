<img width="454" height="403" alt="image" src="https://github.com/user-attachments/assets/cbcdf4d7-bad1-43dd-9cfa-49786a71db9c" />

# ExplorEstable

Un explorador de archivos sencillo, multiplataforma y **de solo lectura**. Está pensado como complemento: **no reemplaza** el explorador de archivos de tu sistema, y por eso no puede copiar, mover, renombrar ni borrar nada.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Plataformas](https://img.shields.io/badge/Windows%20%7C%20macOS%20%7C%20Linux-gray)
![Idiomas](https://img.shields.io/badge/idiomas-10-2f5d50)
![Licencia](https://img.shields.io/badge/licencia-MIT-blue)

Incluye dos versiones con la misma idea:

| Versión | Archivo | Para qué sirve |
|---|---|---|
| Escritorio | `explorestable.py` | Ventana nativa en Windows, macOS y Linux. Solo usa la biblioteca estándar de Python. |
| Web | `explorestable.html` | Un único archivo que se abre en el navegador, sin instalar nada. |

## Características

- Navegación por carpetas, botón **Subir** y barra de ruta editable.
- Buscador por nombre en la carpeta actual.
- Ordenar por nombre, tipo, tamaño o fecha de modificación (carpetas siempre primero).
- Mostrar u ocultar archivos ocultos.
- 10 idiomas, con selector en la propia interfaz.
- Cero dependencias externas.
- Solo lectura: seguro para curiosear en cualquier carpeta.

## Idiomas

| Código | Idioma | Código | Idioma |
|---|---|---|---|
| `es` | Español | `pt` | Português |
| `en` | English | `it` | Italiano |
| `fr` | Français | `zh` | 中文 |
| `de` | Deutsch | `ja` | 日本語 |
| `ru` | Русский | `ko` | 한국어 |

La versión de escritorio elige el idioma según la configuración de tu sistema (si no está disponible, usa inglés). La versión web usa el idioma del navegador y recuerda tu última elección.

## Versión de escritorio (Python)

### Requisitos

- Python 3.8 o superior con **tkinter**.
  - **Windows:** ya viene incluido con el instalador oficial de Python.
  - **macOS:** incluido con el instalador de [python.org](https://www.python.org/). Con Homebrew: `brew install python-tk`.
  - **Linux:** instala el paquete de tkinter, por ejemplo `sudo apt install python3-tk` (Debian/Ubuntu) o `sudo dnf install python3-tkinter` (Fedora).

### Uso

```bash
git clone https://github.com/David4524-maker/explorestable.git
cd explorestable

python explorestable.py              # empieza en tu carpeta personal
python explorestable.py /[ruta]/[carpeta]  # empieza en otra carpeta
```

En algunos sistemas el comando es `python3`.

> AVISO: Los [ruta] y [carpeta] son solo placeholders.

### Atajos

| Acción | Cómo |
|---|---|
| Abrir carpeta o archivo | Doble clic o `Enter` |
| Subir un nivel | Botón **Subir** o `Retroceso` (con la lista seleccionada) |
| Actualizar | Botón **Actualizar** o `F5` |
| Ir a una ruta | Escríbela en la barra superior y pulsa `Enter` |

Los archivos se abren con la aplicación predeterminada de tu sistema. El botón **Abrir en el sistema** abre la carpeta actual en tu explorador de archivos habitual.

## Versión web (HTML)

Abre `explorestable.html` en tu navegador (doble clic o arrastrándolo a una ventana). Verás una carpeta de demostración. Pulsa **Abrir carpeta** para explorar una de tu equipo.

- **Tu información no sale de tu equipo.** El navegador solo lee los nombres, tamaños y fechas de la carpeta que elijas. No se sube nada a ningún servidor.
- Al hacer clic en un archivo, se abre en una pestaña nueva usando el visor del navegador (por ejemplo, imágenes, PDF o texto).
- Sigue el modo claro u oscuro de tu sistema.
- Funciona en navegadores modernos con soporte para selección de carpetas (Chrome, Edge, Firefox y Safari recientes).

## Añadir un idioma

1. **Python:** agrega una línea al diccionario `L` en `explorestable.py` con los 14 textos separados por `|`, en el mismo orden que `KEYS`. Añade también su código en `CODES`.
2. **HTML:** agrega una entrada en `R` (13 textos separados por `|`, en el orden de `K`) y su nombre en `LN`.

## Limitaciones

- Es solo lectura por diseño: no hay operaciones de copiar, mover, renombrar ni eliminar.
- La versión web no puede abrir archivos con aplicaciones del sistema ni explorar rutas por sí sola; depende de la carpeta que elijas.
- Los archivos se detectan como ocultos si empiezan por `.` o, en Windows, si tienen el atributo de oculto.
- Las carpetas muy grandes pueden tardar en cargarse.

## Contribuir

Las sugerencias y los *pull requests* son bienvenidos. Para cambios grandes, abre antes un *issue* y lo comentamos. Si añades una traducción, revisa que el texto quepa bien en los botones.

## Licencia

Distribuido bajo licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

### English summary

**ExplorEstable** is a small, cross-platform, **read-only** file explorer (Explorer + *Estable*, "stable" in Spanish). It does not replace your system's file manager. It ships as a Python/tkinter desktop app (standard library only) and as a single-file HTML app that reads folders locally in your browser, with nothing uploaded. 10 languages: Spanish, English, French, German, Portuguese, Italian, Chinese, Japanese, Russian and Korean. Run it with `python explorestable.py`, or just open `explorestable.html`.

