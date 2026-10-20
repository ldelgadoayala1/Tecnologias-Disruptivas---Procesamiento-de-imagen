"""
07 - Integración: el computador (o la Raspberry Pi) "ve" y el ESP32 "actúa".
Cuando YOLO detecta la clase objetivo, se envía una petición HTTP al ESP32 para encender un LED
(o un buzzer, un relé, un servo...). Cargar antes esp32_actuador/esp32_actuador.ino en el ESP32.
Uso:  python 07_yolo_esp32.py                         (webcam)
      python 07_yolo_esp32.py http://IP:81/stream     (ESP32-CAM como cámara)
"""
import sys, os, time
import requests
from ultralytics import YOLO
from camara import abrir_camara, fuente_desde_argumentos

IP_ESP32 = "192.168.1.50"        # <-- cambiar por la IP que muestra el ESP32 en el Monitor Serie
CLASE_OBJETIVO = "person"        # prueba también con: cell phone, bottle, cup, dog...

ruta = "yolo26n_ncnn_model" if os.path.isdir("yolo26n_ncnn_model") else "yolo26n.pt"
modelo = YOLO(ruta)
leer = abrir_camara(fuente_desde_argumentos(sys.argv))
estado_anterior = None

while True:
    frame = leer()
    if frame is None:
        break
    r = modelo(frame, imgsz=320, conf=0.5, verbose=False)[0]
    detectado = any(modelo.names[int(c.cls)] == CLASE_OBJETIVO for c in r.boxes)

    if detectado != estado_anterior:                     # solo avisar cuando cambia el estado
        estado = "on" if detectado else "off"
        try:
            requests.get(f"http://{IP_ESP32}/led", params={"estado": estado}, timeout=1)
            print(time.strftime("%H:%M:%S"), CLASE_OBJETIVO, "->", estado)
        except requests.RequestException as e:
            print("No se pudo contactar al ESP32:", e)
        estado_anterior = detectado
