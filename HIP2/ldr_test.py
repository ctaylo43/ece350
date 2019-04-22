import RPi.GPIO as GPIO
from gpiozero import LightSensor, Buzzer


#def setup():
	#ldr = LightSensor("BOARD13")
	
def loop():
	ldr = LightSensor(26)
	while True:
		#print(ldr.value)
		print("LDR Value: %.3f" % float(ldr.value))

def destroy():
	GPIO.cleanup()
	
if __name__ == '__main__':
	#setup()
	#try:
	loop()
	#except KeyboardInterrupt:
		#destroy()
