import time

# Pino GPIO onde a luz/LED está ligada — ajuste conforme sua montagem
PINO_LUZ = 17

try:
    from gpiozero import LED
    led = LED(PINO_LUZ)
    RASPBERRY_DISPONIVEL = True
except Exception:
    # Isso acontece quando o código roda fora de um Raspberry Pi
    # (ex: no seu PC, durante o desenvolvimento). Assim dá pra testar
    # o site inteiro sem travar por falta da lib/hardware.
    led = None
    RASPBERRY_DISPONIVEL = False


def AcenderLuz(segundos=3):
    if RASPBERRY_DISPONIVEL:
        led.on()
        time.sleep(segundos)
        led.off()
    else:
        print(f"[SIMULAÇÃO] Luz acesa por {segundos}s (gpiozero indisponível nesse ambiente)")
