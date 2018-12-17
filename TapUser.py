#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
import pandas as pd
import sys
import time


try:
    df = pd.read_csv("databases/users.csv")
    df_events = pd.read_csv("databases/events.csv")
except IOError:
    print("Could not read file: probably didn't exist yet.")
    print("Creating a new one...")
    df = pd.DataFrame(columns=['ID', 'FirstName', 'LastName', 'Email', 'Charge'])
    
try:
    df_events = pd.read_csv("databases/events.csv")
except IOError:
    print("Could not read file: probably didn't exist yet.")
    print("Creating a new one...")
    df_events = pd.DataFrame(columns=['ID', 'Time', 'Volume', 'Cost'])
 
while(True): 
    input = raw_input("Enter 1 for new entry, 2 for exit")
    type(input)
    if input == "2":
        break;
     
    name = raw_input("Enter first name")
    type(name)

    lastName = raw_input("Enter last name")
    type(lastName)

    email = raw_input("Enter email address")
    type(email)


    reader = SimpleMFRC522.SimpleMFRC522()

    print("Scan badge to capture ID")

    print(reader.read()[0])
    flag = True
    while(flag):
        id, text = reader.read()
        if id is not None:
            print(df['ID'])
            print(id in df['ID'].values)
            if id not in df['ID'].values:
                flag = False
                print(id)
                print(text)
            else:
                print("Badge already in system! Place another badge...")
        time.sleep(0.5)

    print("Adding to record...")
    df = df.append({'ID': id, 'FirstName' : name, 'LastName': lastName, 'Email': email}, ignore_index = True)
    print(df)

    df.to_csv("databases/users.csv")
    df_events.to_csv("databases/events.csv")


GPIO.cleanup()
