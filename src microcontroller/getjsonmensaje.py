from machine import Pin, I2C
from time import sleep, sleep_ms
from esp8266_i2c_lcd import I2cLcd
import network
import socket
import json


URL = 'http://<Tu usuario>.pythonanywhere.com/getjson'
# CREDENCIALES
USUARIO = '<nombre de tu WiFi>'
CONTRASENIA = '<Contraseña del modem>'


i2c = I2C(scl=Pin(5),sda=Pin(4),freq=400000)
lcd = I2cLcd(i2c,0x27,2,16)
retornado = ''
led_D0 = Pin(16, Pin.OUT)
led_D0.off()

lcd.putstr("Programado por\nEsimio Impune")
sleep(1)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(USUARIO, CONTRASENIA)
while not sta_if.isconnected():
    pass
if sta_if.isconnected():
    lcd.clear()
    lcd.putstr("Control online\nremoto:")
    sleep(2)
    lcd.putstr(" OK")
    sleep(1)
    # print('\n')
    # print(USUARIO)
    # print("  Conectado")
    lcd.clear()
#print('Configuracion de red:\n', sta_if.ifconfig())

def http_get(url):
    global retornado
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            #al parecer al hacer esto se pierde la primer {
            retornado = str(data, 'utf8')
            #print(retornado, end='')
        else:
            break
    s.close()


def dar_formato_a(msg):
    if len(msg) > 16:
        return msg[:16] + '\n' + msg[16:]
    else:
        return msg


def encender_o_apagar_LED(orden):
    if orden == 1:
        led_D0.on()
        return True
    elif orden == 0:
        led_D0.off()
        return False


primera_iteracion = True
estado_anterior = None
msg_anterior = 'None'
while True:
    http_get(URL)
    try:
        diccionario_json = json.loads(retornado)
    except ValueError:
        #solucionando la perdida q ocurre en el if dentro del while en http_get()
        retornado = '{' + retornado
        diccionario_json = json.loads(retornado)
    finally:
        try:
        #pin16 registra el estado actual (led encendido o apagado)
            pin16 = diccionario_json["pin16"]
            msg = diccionario_json["msg"]
            if primera_iteracion is True:
                lcd.clear()
                lcd.putstr(msg)
            else:
        #la siguiente linea es para q el LCD no esté actualizandose innecesariamente
                if msg_anterior != msg:
                    lcd.clear()
                    lcd.putstr(dar_formato_a(msg))
            msg_anterior = msg
            estado_anterior = encender_o_apagar_LED(pin16) #registro del último estado
        except NameError:
            err_json = "NameError"
            lcd.clear()
            lcd.putstr(err_json)
            #print(d)
        sleep_ms(50)
        primera_iteracion = False
