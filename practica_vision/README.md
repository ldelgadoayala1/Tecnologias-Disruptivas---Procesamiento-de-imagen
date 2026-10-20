# Práctica: procesamiento de imágenes, OCR y YOLO — Tecnologías Disruptivas (UNAB)

Todo funciona en **tu propio computador** con una **webcam** (integrada, USB o el celular como cámara).
Más adelante, la misma carpeta sirve con la **ESP32-CAM** como cámara.

## 1. Instalación (una sola vez)

Necesitas **Python 3.10 o superior**.

```bash
python -m venv vision
vision\Scripts\activate          # Windows
# source vision/bin/activate     # macOS / Linux
pip install ultralytics pytesseract requests
```
Cada vez que abras una terminal nueva, vuelve a activar el entorno (`vision\Scripts\activate`).

**Tesseract** (para el OCR) se instala aparte:
- **Windows:** instalador de UB Mannheim (github.com/UB-Mannheim/tesseract/wiki). En "Additional language data" marca *Spanish*. Agrega `C:\Program Files\Tesseract-OCR` al PATH y reinicia la terminal (ver abajo).
- **macOS:** `brew install tesseract tesseract-lang`
- **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-spa`

**Agregar Tesseract al PATH en Windows desde la terminal**

Permanente (recomendado), en PowerShell y sin permisos de administrador:
```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Program Files\Tesseract-OCR", "User")
```
Luego **cierra y vuelve a abrir la terminal** (y VS Code, si usas su terminal). No uses `setx PATH "%PATH%;..."`: puede cortar el PATH si supera 1024 caracteres.

Solo para la terminal actual (se pierde al cerrarla):
```powershell
$env:Path += ";C:\Program Files\Tesseract-OCR"            # PowerShell
```
```bash
export PATH="$PATH:/c/Program Files/Tesseract-OCR"         # Git Bash / MSYS2
```

Comprueba que funciona:
```powershell
tesseract --version
tesseract --list-langs     # debe aparecer "spa"
```

Alternativa sin tocar el PATH: en `03_ocr.py`, después de `import pytesseract`, agrega
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

Comprueba todo con:
```bash
python 00_verificar_entorno.py
```

## 2. ¿Qué cámara uso?

Todos los scripts que usan cámara aceptan la fuente como argumento:

| Cámara | Cómo se indica |
|---|---|
| Webcam integrada o USB | nada (`python 05_yolo_camara.py`) o un número: `1`, `2` |
| Celular como cámara (app tipo "IP Webcam") | `http://IP_DEL_CELULAR:8080/video` |
| ESP32-CAM (ejemplo CameraWebServer) | `http://IP_DE_LA_ESP32CAM:81/stream` |
| Un video grabado | `mi_video.mp4` |
| Camera Module de Raspberry Pi | `picam` |

El celular y el computador (o la ESP32-CAM) deben estar en la **misma red WiFi**.

## 3. Archivos y orden sugerido (≈10 min cada uno)

| Archivo | Qué hace | Ejemplo |
|---|---|---|
| `00_verificar_entorno.py` | Revisa Python, OpenCV, Tesseract, Ultralytics y la cámara | `python 00_verificar_entorno.py` |
| `01_ver_camara.py` | Muestra la cámara en vivo; tecla **f** guarda una foto en `imagenes/` | `python 01_ver_camara.py` |
| `02_procesamiento.py` | Grises, umbral, bordes y contornos (OpenCV, sin IA) | `python 02_procesamiento.py imagenes/etiqueta.jpg` |
| `03_ocr.py` | Lee texto con Tesseract (imagen o foto de la cámara) | `python 03_ocr.py imagenes/etiqueta.jpg` |
| `04_yolo_imagen.py` | Detecta objetos en una imagen con YOLO26n | `python 04_yolo_imagen.py imagenes/calle.jpg` |
| `05_yolo_camara.py` | YOLO en tiempo real, cuenta objetos y muestra FPS | `python 05_yolo_camara.py` |
| `06_exportar_ncnn.py` | Optimiza el modelo (sobre todo para Raspberry Pi) | `python 06_exportar_ncnn.py` |
| `07_yolo_esp32.py` | Si detecta un objeto, envía una orden HTTP al ESP32 | `python 07_yolo_esp32.py` |
| `esp32_actuador/esp32_actuador.ino` | Servidor web en el ESP32 que enciende/apaga un LED | Arduino IDE |
| `yolo_api.py` | Extensión: YOLO como API con FastAPI | `uvicorn yolo_api:app --port 8000` |
| `camara.py` | Módulo de apoyo que abre cualquier cámara (no se ejecuta solo) | — |

Los resultados quedan en la carpeta `resultados/`. Para la API: `pip install fastapi uvicorn python-multipart`.

## 4. ESP32-CAM (cuando llegue)

1. Arduino IDE → *Archivo → Ejemplos → ESP32 → Camera → CameraWebServer*.
2. Descomenta el modelo de tu placa (normalmente `CAMERA_MODEL_AI_THINKER`) y escribe tu red WiFi.
3. Carga el programa y copia la IP del Monitor Serie (115200 baudios).
4. Pruébala en el navegador (`http://IP`) y luego en Python: `python 05_yolo_camara.py http://IP:81/stream`

La ESP32-CAM **solo envía la imagen**: YOLO se ejecuta en el computador o en la Raspberry Pi.

## 5. Problemas frecuentes
- **`TesseractNotFoundError`**: Tesseract no está instalado o no está en el PATH (reinicia la terminal).
- **La webcam no abre**: ciérrala en otras apps (Teams, Zoom, navegador) o prueba con `1` en vez de `0`.
- **Muy lento**: baja `TAMANO` a 320 en `05_yolo_camara.py`; en la Pi usa `06_exportar_ncnn.py`.
- **La cámara por WiFi se congela**: acerca el equipo al router y baja la resolución en la página de la ESP32-CAM.
- **`pip` dice "externally-managed-environment"**: falta activar el entorno virtual.
