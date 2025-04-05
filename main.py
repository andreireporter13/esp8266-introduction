import machine
import network
import socket
import time

CONFIG_FILE = 'wifi_config.txt'
LED_PIN = 2

WIFI_SSID = None
WIFI_PASS = None

try:
    with open(CONFIG_FILE, 'r') as f:
        data = f.readlines()
        WIFI_SSID = data[0].strip()
        WIFI_PASS = data[1].strip()
    if not WIFI_SSID or not WIFI_PASS:
        print(f"ERROR: File '{CONFIG_FILE}' is incomplete or empty.")
        WIFI_SSID = None
        WIFI_PASS = None
    else:
         print(f"Credentials loaded from '{CONFIG_FILE}'.")
except OSError:
    print(f"ERROR: File '{CONFIG_FILE}' not found.")
    print("Ensure you have created and uploaded the file with SSID on the first line and Password on the second.")
except Exception as e:
    print(f"ERROR unexpected error reading '{CONFIG_FILE}': {e}")
    WIFI_SSID = None
    WIFI_PASS = None

led = machine.Pin(LED_PIN, machine.Pin.OUT)
led.value(1)
led_state = False

def connect_wifi():
    if not WIFI_SSID or not WIFI_PASS:
        print("Wi-Fi credentials not available. Cannot connect.")
        return None

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to Wi-Fi network', WIFI_SSID, '...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASS)
        max_wait = 15
        while not sta_if.isconnected() and max_wait > 0:
            print('.', end='')
            time.sleep(1)
            max_wait -= 1

        if sta_if.isconnected():
            print('\nConnected! IP Address:', sta_if.ifconfig()[0])
            return sta_if.ifconfig()[0]
        else:
            print('\nCould not connect to Wi-Fi.')
            return None
    else:
        print('Already connected. IP Address:', sta_if.ifconfig()[0])
        return sta_if.ifconfig()[0]

def web_server(ip_address):
    global led_state

    if not ip_address:
        print("Cannot start web server without a Wi-Fi connection.")
        return

    addr = socket.getaddrinfo(ip_address, 80)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('Web server running on http://' + ip_address)

    while True:
        conn = None # Ensure conn is defined before try block
        try:
            conn, addr_client = s.accept()
            print('Connection from:', addr_client)
            request = conn.recv(1024)
            request = str(request)
            print('Request received:', request)

            led_on = request.find('/led/on')
            led_off = request.find('/led/off')

            response = ""
            content = ""

            if led_on == 6:
                print('Command received: Turn LED ON')
                led.value(0)
                led_state = True
                content = "LED ON"
            elif led_off == 6:
                print('Command received: Turn LED OFF')
                led.value(1)
                led_state = False
                content = "LED OFF"
            else:
                content = """<!DOCTYPE html><html><head><title>ESP8266 LED Control</title></head><body>
                           <h1>ESP8266 LED Control</h1>
                           <p>LED Status: {}</p>
                           <p><a href="/led/on"><button>Turn LED ON</button></a>
                              <a href="/led/off"><button>Turn LED OFF</button></a></p>
                           </body></html>""".format('ON' if led_state else 'OFF')

            response = 'HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n' + content

            conn.sendall(response.encode())
            conn.close()

        except OSError as e:
            if conn:
                 conn.close()
            print('Connection error:', e)
        except Exception as e:
             if conn:
                 conn.close() # Also close connection on general exceptions
             print(f"Unknown error in server loop: {e}")


if WIFI_SSID and WIFI_PASS:
    ip = connect_wifi()
    if ip:
        web_server(ip)
    else:
        print("Web server startup failed due to Wi-Fi connection issues.")
else:
    print("Web server cannot start because Wi-Fi credentials are missing or could not be read.")
