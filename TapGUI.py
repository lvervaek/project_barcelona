#!/usr/bin/env python
# Import the pygame library and initialise the game engine

import RPi.GPIO as GPIO
import SimpleMFRC522
import MFRC522
import pygame
import sys
import time
import pandas as pd
pygame.init()

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

reader = SimpleMFRC522.SimpleMFRC522()
complex_reader = MFRC522.MFRC522()

try:
    df_users = pd.read_csv("databases/users.csv")
except IOError:
    print("Could not read file: probably didn't exist yet.")
    print("Creating a new one...")
    df_users = pd.DataFrame(columns=['ID', 'FirstName', 'LastName', 'Email'])




# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")

font = pygame.font.SysFont("Lato-Medium",36)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Homescreen
def displayHomeScreen():
    card_text = font.render("Place card to start pouring!", True, (0,0,200))
    screen.fill(WHITE)
    screen.blit(card_text, (50,150))
    pygame.display.flip()

def displayPouringScreen(name):
    card_text = font.render("Hi " + str(name) + ", start pouring with P", True, (0,0,200))
    screen.fill(WHITE)
    screen.blit(card_text, (50,150))
    pygame.display.flip()
    
 
# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
              
    # --- Game logic should go here
    displayHomeScreen()
        
    while(True):
        displayHomeScreen()
        print(reader.read()[0])
        
        time.sleep(1)
        while(reader.read()[0] is not None):
            print(reader.read())
            id, data = reader.read()
            name = df_users[df_users['ID'] == id]['FirstName'].values[0]
            text = raw_input("Press P to start pouring")
            if text == 'P':
                new_pour = int(data)+1
                reader.write(str(new_pour))
                print("Drink total:" + str(new_pour))            

    
    # --- Drawing code should go here
    # First, clear the screen to white. 
    #The you can draw different shapes and lines or add text to your background stage.
    pygame.draw.rect(screen, RED, [55, 200, 100, 70],0)
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
GPIO.cleanup()
pygame.quit()