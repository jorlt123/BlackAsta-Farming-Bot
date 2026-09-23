import time
import threading
import pyautogui
from collections import deque

# =========================
# CONFIGURACIÓN
# =========================

WORK_INTERVAL = 61       # .work cada 61 s
MINE_INTERVAL = 301      # .mine cada 5 min 1 s
CRIME_INTERVAL = 181     # ciclo cada 3 min 1 s

MAX_MENSAJES = 4
VENTANA = 2.0

# Pausa general:
# 2 horas activo -> 10 minutos parado
TIEMPO_ACTIVO = 2 * 60 * 60
TIEMPO_PAUSA = 10 * 60

activo = True
inicio_periodo = time.monotonic()

# Protege el teclado y el contador de mensajes
bloqueo = threading.Lock()

# Guarda los momentos de los últimos envíos
historial = deque()


# =========================
# ENVÍO CON PROTECCIÓN
# =========================

def enviar(mensaje):
    global historial

    with bloqueo:
        while True:
            ahora = time.monotonic()

            # Eliminar mensajes que ya están fuera de la ventana
            while historial and ahora - historial[0] >= VENTANA:
                historial.popleft()

            # Máximo 4 mensajes en 2 segundos
            if len(historial) < MAX_MENSAJES:
                pyautogui.write(mensaje, interval=0.05)
                pyautogui.press("enter")

                historial.append(time.monotonic())
                print(f"Enviado: {mensaje}")
                return

            # Esperar hasta que salga el mensaje más antiguo
            espera = VENTANA - (ahora - historial[0])
            time.sleep(max(espera, 0.01))


# =========================
# PAUSA GENERAL
# =========================

def comprobar_pausa():
    global activo, inicio_periodo

    ahora = time.monotonic()
    transcurrido = ahora - inicio_periodo

    if activo:
        if transcurrido >= TIEMPO_ACTIVO:
            activo = False
            print("⏸️ Pausa de 10 minutos.")
            return False
    else:
        if transcurrido >= TIEMPO_PAUSA:
            activo = True
            inicio_periodo = time.monotonic()
            print("▶️ Bot reanudado.")
            return True

    return activo


# =========================
# .WORK
# =========================

def work():
    while True:
        if comprobar_pausa():
            enviar(".work")
        time.sleep(WORK_INTERVAL)


# =========================
# .MINE
# =========================

def mine():
    while True:
        if comprobar_pausa():
            enviar(".mine")
        time.sleep(MINE_INTERVAL)


# =========================
# .D + .CRIME + .SLUT
# =========================

def crime():
    while True:

        if comprobar_pausa():
            enviar(".d")

            time.sleep(2)

            if comprobar_pausa():
                enviar(".crime")

            time.sleep(2)

            if comprobar_pausa():
                enviar(".slut")

        time.sleep(CRIME_INTERVAL)


# =========================
# INICIO
# =========================

print("🤖 Bot iniciado")
print(".work  → cada 61 segundos")
print(".mine  → cada 5 minutos y 1 segundo")
print(".d     → 2 segundos antes de .crime")
print(".crime → cada 3 minutos y 1 segundo")
print(".slut  → 2 segundos después de .crime")
print("⏸️ 2 horas activo → 10 minutos de pausa")
print("🛡️ Máximo 4 mensajes en cualquier ventana de 2 segundos")

threading.Thread(target=work, daemon=True).start()
threading.Thread(target=mine, daemon=True).start()
threading.Thread(target=crime, daemon=True).start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Bot detenido.")