# Info about ESP8266

# Download firmware
https://micropython.org/download/ESP8266_GENERIC/

# Erase
esptool.py --port /dev/ttyUSB0 erase_flash

# New firmware
sudo /home/$USER/Documents/$PATH_TO_ENV/venv/bin/esptool.py \
--port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC-20241129-v1.24.1.bin

# ...
sudo usermod -aG uucp $USER

# Connect to ESP
screen /dev/ttyUSB0 115200
`
# connect to ESP repl for testing
mpremote connect /dev/ttyUSB0 repl

# connect to ESP8266 and testing...
mpremote connect /dev/ttyUSB0
mpremote connect /dev/ttyUSB0 ls :
mpremote connect /dev/ttyUSB0 cp main.py . :

# copy to ESP8266
mpremote connect /dev/ttyUSB0 cp main.py :
mpremote connect /dev/ttyUSB0 cp wifi_config.txt :

# in case if some problem with USB0
sudo lsof /dev/ttyUSB0
