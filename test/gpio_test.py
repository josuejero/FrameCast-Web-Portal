import RPi.GPIO as GPIO
import time

BUTTON_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_state = GPIO.HIGH

try:
	while True:
		current_state = GPIO.input(BUTTON_PIN)
		if previous_state==GPIO.HIGH and current_state == GPIO.LOW:
			print("Button Pressed")
		
		previous_state = current_state
		
		time.sleep(1)
except KeyboardInterrupt:
	Pass
finally:
	GPIO.cleanup()
