# 🚀 ESP8266 + MicroPython Setup Guide

```bash
Download the latest MicroPython firmware for ESP8266 from:
https://micropython.org/download/ESP8266_GENERIC/
```

Erase the flash memory:
```bash
esptool.py --port /dev/ttyUSB0 erase_flash
```

Flash the new firmware (adjust the path to your virtual env):
```bash
sudo /home/$USER/Documents/$PATH_TO_ENV/venv/bin/esptool.py \
--port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ESP8266_GENERIC-20241129-v1.24.1.bin
```

Fix serial port permissions:
```bash
sudo usermod -aG uucp $USER
```

# ⚠️ Log out and log back in (or reboot) after this step

Connect to ESP8266 using screen:
```bash
screen /dev/ttyUSB0 115200
```

Or (recommended) connect with mpremote:
```bash
mpremote connect /dev/ttyUSB0 repl
```

List files on the ESP8266:
```bash
mpremote connect /dev/ttyUSB0 ls :
```

Copy files to ESP8266:
```bash
mpremote connect /dev/ttyUSB0 cp main.py :
mpremote connect /dev/ttyUSB0 cp wifi_config.txt :
```
Copy file from ESP8266 to your local machine:
```bash
mpremote connect /dev/ttyUSB0 cp main.py . :
```

Check what's using the serial port if you run into issues:
```bash
sudo lsof /dev/ttyUSB0
```

# ✅ Done. You're ready to roll.
