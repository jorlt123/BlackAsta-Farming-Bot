import time
import pyautogui
import threading

# =========================
# CONFIGURACIÓN
# =========================

WORK = 61       # .work cada 61 s
MINE = 301      # .mine cada 5 min 1 s
CRIME = 181     # ciclo de .crime cada 3 min 1 s

ACTIVO = True
inicio_ciclo = time.monotonic()

# Evita que dos comandos se escriban simultáneamente
bloqueo = threading.Lock()

# Último momento en que se envió un comando
ultimo_envio = 0

# Mínimo espacio entre comandos
ESPACIO_MINIMO = 1.0


# =========================
# ENVÍO SEGURO
# =========================

def enviar(mensaje):
    global ultimo_envio

    with bloqueo:
        ahora = time.monotonic()
        espera = ESPACIO_MINIMO - (ahora - ultimo_envio)

        if espera > 0:
            time.sleep(espera)

        pyautogui.write(mensaje, interval=0.05)
        pyautogui.press("enter")

        ultimo_envio = time.monotonic()

        print(f"Enviado: {mensaje}")


# =========================
# CONTROL DE PAUSAS
# =========================

def esta_activo():
    global ACTIVO, inicio_ciclo

    transcurrido = time.monotonic() - inicio_ciclo

    # 2 horas activo
    if ACTIVO and transcurrido >= 7200:
        ACTIVO = False
        print("⏸️ Pausa de 10 minutos.")

    # 10 minutos parado
    elif not ACTIVO and transcurrido >= 7800:
        ACTIVO = True
        inicio_ciclo = time.monotonic()
        print("▶️ Bot reanudado.")

    return ACTIVO


# =========================
# .WORK
# =========================

def work():
    siguiente = time.monotonic()

    while True:
        if esta_activo() and time.monotonic() >= siguiente:
            enviar(".work")
            siguiente += WORK

        time.sleep(0.05)


# =========================
# .MINE
# =========================

def mine():
    # Empieza 10 segundos después
    siguiente = time.monotonic() + 10

    while True:
        if esta_activo() and time.monotonic() >= siguiente:
            enviar(".mine")
            siguiente += MINE

        time.sleep(0.05)


# =========================
# .D + .CRIME + .SLUT
# =========================

def crime():
    # Empieza 20 segundos después
    siguiente = time.monotonic() + 20

    while True:
        if esta_activo() and time.monotonic() >= siguiente:

            # .d
            enviar(".d")

            # 2 segundos después
            time.sleep(2)

            if esta_activo():
                enviar(".crime")

            # 2 segundos después
            time.sleep(2)

            if esta_activo():
                enviar(".slut")

            # Mantiene el ciclo de 181 segundos
            siguiente += CRIME

        time.sleep(0.05)


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
print("🔒 Protección anti-solapamiento activada")

threading.Thread(target=work, daemon=True).start()
threading.Thread(target=mine, daemon=True).start()
threading.Thread(target=crime, daemon=True).start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Bot detenido.")