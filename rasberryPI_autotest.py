import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

mode = GPIO.getmode()
print(mode)

#set GPIO mode - for LED out, for button in
GPIO.setup(11, GPIO.IN)
GPIO.setup(2, GPIO.OUT)

while True:
    gpio_11 = GPIO.input(11)
    #press = 0 unpress = 1
    #print(gpio_11)

    if gpio_11 == 0:
        time.sleep(0.2)
        GPIO.output(2, 0)
        time.sleep(0.2)
        GPIO.output(2, 1)