#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


#GPIO.setwarnings(False)

reader = SimpleMFRC522()

granted_led_pin = 12
denied_led_pin = 18
buzzer_pin = 16

GPIO.setup(granted_led_pin, GPIO.OUT)
GPIO.setup(denied_led_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
        id, text = reader.read()
        print(id)
        print(text)
finally:
        GPIO.cleanup()

def read():
        id, text = reader.read()
        time.sleep(0.3)
        return id, text

        

# #!/usr/bin/env python
# # -*- coding: utf8 -*-
 
# import RPi.GPIO as GPIO
# import MFRC522
# import signal
# import time
 
# continue_reading = True
 
# # Capture SIGINT for cleanup when the script is aborted
# def end_read(signal,frame):
#     global continue_reading
#     print ("Ctrl+C captured, ending read.")
#     continue_reading = False
#     GPIO.cleanup()
 
# # Hook the SIGINT
# signal.signal(signal.SIGINT, end_read)
 
# # Create an object of the class MFRC522
# MIFAREReader = MFRC522.MFRC522()
 
# # Welcome message
# print ("Welcome to the MFRC522 data read example")
# print ("Press Ctrl-C to stop.")
 
# # This loop keeps checking for chips. If one is near it will get the UID and authenticate
# while continue_reading:
    
#     # Scan for cards    
#     (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
#     # If a card is found
#     if status == MIFAREReader.MI_OK:
#         print ("Card detected")
    
#     # Get the UID of the card
#     (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
#     # If we have the UID, continue
#     if status == MIFAREReader.MI_OK:
 
#         # Print UID
#         print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
#         # This is the default key for authentication
#         key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
#         # Select the scanned tag
#         MIFAREReader.MFRC522_SelectTag(uid)
        
#         #ENTER Your Card UID here
#         my_uid = [61,84,4,114,31]
        
#         #Configure LED Output Pin
#         LED = 18
#         GPIO.setup(LED, GPIO.OUT)
#         GPIO.output(LED, GPIO.LOW)
        
#         #Check to see if card UID read matches your card UID
#         if uid == my_uid:                #Open the Doggy Door if matching UIDs
#             print("Access Granted")
#             GPIO.output(LED, GPIO.HIGH)  #Turn on LED
#             time.sleep(5)                #Wait 5 Seconds
#             GPIO.output(LED, GPIO.LOW)   #Turn off LED
            
#         else:                            #Don't open if UIDs don't match
#             print("Access Denied, YOU SHALL NOT PASS!")
        
# ##        # Authenticate
# ##        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
# ##
# ##        # Check if authenticated
# ##        if status == MIFAREReader.MI_OK:
# ##            MIFAREReader.MFRC522_Read(8)
# ##            MIFAREReader.MFRC522_StopCrypto1()
# ##        else:
# ##            print "Authentication error"
