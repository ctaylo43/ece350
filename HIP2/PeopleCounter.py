import RPi.GPIO as GPIO
import time
from picamera import PiCamera

#~~~~ 4 Bit 7 Segment Display Definitions ~~~~~
BIT0 = 3   
BIT1 = 5  
BIT2 = 24  
BIT3 = 26  

segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]  #0~9  
pins = [11,12,13,15,16,18,22,7,3,5,24,26]  
bits = [BIT0, BIT1, BIT2, BIT3]  

#~~~~ Other Pin Defintions ~~~~
IR1Pin = 29	# entrance IR
IR2Pin = 31	# exit IR
BZRPin = 33	# Buzzer

#~~~~ Camera ~~~~
camera = PiCamera()

#~~~~ Global Variables ~~~~
ppl_cnt = 0 # number of people
IR1_detect = False
IR2_detect = False

ldr = LightSensor(37)

p = None

def print_msg():  
	print 'Program is running...'  
	print 'Please press Ctrl+C to end the program...'  

def digitalWriteByte(val):  
	GPIO.output(11, val & (0x01 << 0))  
	GPIO.output(12, val & (0x01 << 1))  
	GPIO.output(13, val & (0x01 << 2))  
	GPIO.output(15, val & (0x01 << 3))  
	GPIO.output(16, val & (0x01 << 4))  
	GPIO.output(18, val & (0x01 << 5))  
	GPIO.output(22, val & (0x01 << 6))  
	GPIO.output(7,  val & (0x01 << 7))  

def display(num):  
	b0 = num % 10  
	b1 = num % 100 / 10   
	b2 = num % 1000 / 100  
	b3 = num / 1000  
	if num < 10:  
		GPIO.output(BIT0, GPIO.LOW)   
		GPIO.output(BIT1, GPIO.HIGH)   
		GPIO.output(BIT2, GPIO.HIGH)   
		GPIO.output(BIT3, GPIO.HIGH)   
	 	digitalWriteByte(segCode[b0])  
	elif num >= 10 and num < 100:  
		GPIO.output(BIT0, GPIO.LOW)  
		digitalWriteByte(segCode[b0])  
		time.sleep(0.002)  
		GPIO.output(BIT0, GPIO.HIGH)   
		GPIO.output(BIT1, GPIO.LOW)  
		digitalWriteByte(segCode[b1])  
		time.sleep(0.002)  
	 	GPIO.output(BIT1, GPIO.HIGH)  
	elif num >= 100 and num < 1000:  
		GPIO.output(BIT0, GPIO.LOW)  
		digitalWriteByte(segCode[b0])  
		time.sleep(0.002)  
		GPIO.output(BIT0, GPIO.HIGH)   
		GPIO.output(BIT1, GPIO.LOW)  
		digitalWriteByte(segCode[b1])  
		time.sleep(0.002)  
		GPIO.output(BIT1, GPIO.HIGH)  
		GPIO.output(BIT2, GPIO.LOW)  
		digitalWriteByte(segCode[b2])  
		time.sleep(0.002)  
	 	GPIO.output(BIT2, GPIO.HIGH)   
	elif num >= 1000 and num < 10000:  
		GPIO.output(BIT0, GPIO.LOW)  
		digitalWriteByte(segCode[b0])  
		time.sleep(0.002)  
		GPIO.output(BIT0, GPIO.HIGH)   
		GPIO.output(BIT1, GPIO.LOW)  
		digitalWriteByte(segCode[b1])  
		time.sleep(0.002)  
		GPIO.output(BIT1, GPIO.HIGH)  
		GPIO.output(BIT2, GPIO.LOW)  
		digitalWriteByte(segCode[b2])  
		time.sleep(0.002)  
		GPIO.output(BIT2, GPIO.HIGH)   
		GPIO.output(BIT3, GPIO.LOW)  
		digitalWriteByte(segCode[b3])  
		time.sleep(0.002)  
	 	GPIO.output(BIT3, GPIO.HIGH)   
	else:  
		 print 'Out of range, num should be 0~9999 !'  

def setup():
	GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location  
	GPIO.setwarnings(False)
	for pin in pins:  # Setup 7 Seg pins
		GPIO.setup(pin, GPIO.OUT)    #set all pins' mode is output  
		GPIO.output(pin, GPIO.HIGH)  #set all pins are high level(3.3V) 
    ADC0832.setup()	# setup ADC

    # IR Sensor setup
    GPIO.setup(IR1Pin, GPIO.IN)
    GPIO.setup(IR2Pin, GPIO.IN)

    # Buzzer setup
    GPIO.setup(BZRPin, GPIO.OUT)   # Set pin mode as output
	GPIO.output(BZRPin, GPIO.LOW)

def IR1_isr():
	IR1_detect = True

def IR2_isr():
	IR2_detect = True

def enter_sound():
	p.changeFrequency(1500)
	p.start(50) # 50% Duty Cycle
	time.sleep(0.5)
	p.changeFrequency(2000)
	time.sleep(0.5)
	p.stop()

def exit_sound():
	p.changeFrequency(2000)
	p.start(50) # 50% Duty Cycle
	time.sleep(0.5)
	p.changeFrequency(1500)
	time.sleep(0.5)
	p.stop()

def loop():
	#GPIO.add_event_detect(IR1Pin, GPIO.FALLING, callback=IR1_isr)
	#GPIO.add_event_detect(IR2Pin, GPIO.FALLING, callback=IR2_isr)
	global p
	p = GPIO.PWM(BZRPin, 50)
	while True:
		# put everything below here in an else statement having correct amount of light
		if GPIO.input(IR1Pin) == GPIO.HIGH:
			ppl_cnt += 1
			enter_sound()
		elif GPIO.input(IR2Pin) == GPIO.HIGH:
			ppl_cnt -= 1
			exit_sound()
		display(ppl_cnt)


def destroy():
	for pin in pins:    
		GPIO.output(pin, GPIO.LOW) #set all pins are low level(0V)   
		GPIO.setup(pin, GPIO.IN)   #set all pins' mode is input  
	GPIO.cleanup()                     	# Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
		ADC0832.destroy()