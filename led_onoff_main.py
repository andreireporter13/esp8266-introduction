from machine import Pin
import time

led_builtin = Pin(2, Pin.OUT)

print("Program Start!")

while True:
  try:
    led_builtin.value(0)
    print("LED ON")
    time.sleep(1)

    led_builtin.value(1)
    print("LED OFF")
    time.sleep(1)

  except KeyboardInterrupt:
    print("Program Stopped.")
    led_builtin.value(1)
    break
