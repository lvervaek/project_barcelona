#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

print("Place badge to start pouring")
try:
    while(reader.read()):
        id, pour = reader.read()
        text = raw_input("Press P to start pouring")
        if text == 'P':
            new_pour = int(pour)+1
            reader.write(str(new_pour))
            print("Drink total:" + str(new_pour))
finally:
    GPIO.cleanup()
            
            
    