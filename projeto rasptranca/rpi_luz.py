import time

# Pinos GPIO onde cada luz/LED está ligada — ajuste conforme sua montagem
PINO_LUZ_VERDE = 17     # acende quando a digital É encontrada
PINO_LUZ_VERMELHA = 27  # acende quando a digital NÃO é encontrada

try:
    from gpiozero import LED
    led_verde = LED(PINO_LUZ_VERDE)
    led_vermelha = LED(PINO_LUZ_VERMELHA)
    RASPBERRY_DISPONIVEL = True
except Exception:
    # Isso acontece quando o código roda fora de um Raspberry Pi
    # (ex: no seu PC, durante o desenvolvimento). Assim dá pra testar
    # o site inteiro sem travar por falta da lib/hardware.
    led_verde = None
    led_vermelha = None
    RASPBERRY_DISPONIVEL = False


def _piscar(led, nome, segundos):
    if RASPBERRY_DISPONIVEL:
        led.on()
        time.sleep(segundos)
        led.off()
    else:
        print(f"[SIMULAÇÃO] Luz {nome} acesa por {segundos}s (gpiozero indisponível nesse ambiente)")


def AcenderLuz(digital_encontrada, segundos=3):
    """
    Acende a luz verde se a digital foi encontrada no banco,
    ou a luz vermelha caso contrário.
    """
    if digital_encontrada:
        _piscar(led_verde, "VERDE", segundos)
    else:
        _piscar(led_vermelha, "VERMELHA", segundos)
