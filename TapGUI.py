#!/usr/bin/env python
# Import the pygame library and initialise the game engine

import RPi.GPIO as GPIO
import SimpleMFRC522
import MFRC522
import pygame
import sys
import time
import pandas as pd

GPIO.setmode(GPIO.BCM)
inpt = 27
GPIO.setup(inpt, GPIO.IN)
rate_cnt = 0
tot_cnt = 0
time_zero = 0.0
time_start = 0.0
time_end = 0.0
gpio_last = 0
pulses = 0
constant = 0.23
costPerCl = 8
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
    df_events = pd.read_csv("databases/events.csv")
except IOError:
    print("Could not read file: probably didn't exist yet.")
    print("Exiting...")
    GPIO.cleanup()
    pygame.quit()




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

def displayPouringScreen(name, volume):
    card_text = font.render("Hi " + str(name) + ", start pouring!", True, (0,0,200))
    volume_text = font.render("You've tapped " + str(volume) + " cl, for " + str(volume*costPerCl) + ".", True, (0,100,200))
    screen.fill(WHITE)
    screen.blit(card_text, (50,150))
    screen.blit(volume_text, (50,200))
    pygame.display.flip()

def displayBadgeNotRec():
    card_text = font.render("Hi stranger, you badge was not recognized.", True, (0,0,200))
    volume_text = font.render("I'm sorry but I can't let you TAP that.", True, (0,100,200))
    screen.fill(WHITE)
    screen.blit(card_text, (50,150))
    screen.blit(volume_text, (50,200))
    pygame.display.flip()
    
 
# -------- Main Program Loop -----------
time_zero = time.time()
while carryOn:
    # --- Main event loop
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
              carryOn = False # Flag that we are done so we exit this loop
              
    # --- Game logic should go here
    displayHomeScreen()
        
    while(True):
        displayHomeScreen()
        id, data = 0,0
        print(reader.read()[0])
        
        time.sleep(1)
        while(reader.read()[0] is not None):
            rate_cnt = 0
            pulses = 0
            time_start = time.time()
            
            #Check if user exists, and if he has charge left
            id, data = reader.read()
            if id not in df_users['ID'].values:
                displayBadgeNotRec()
                break
            name = df_users[df_users['ID'] == id]['FirstName'].values[0]
            displayPouringScreen(name, round(tot_cnt * constant, 3))
            #if df_users[df_users['ID'] == id]['Charge'] > 0:
            #open relay
            #
            #
            
            while pulses <= 5:
                gpio_cur = GPIO.input(inpt)
                if gpio_cur != 0 and gpio_cur != gpio_last:
                    pulses += 1
                gpio_last = gpio_cur
                try:
                    #print(GPIO.input(inpt))
                    None
                except:
                    print('\nCTRL C -Nice exit')
                    GPIO.cleanup()
                    print('Done')
                    sys.exit()
                    
            rate_cnt += 1
            tot_cnt += 1
            time_end = time.time()
            print('\nLiters / min ', round((rate_cnt * constant)/(time_end - time_start), 2), 'approx ')
            print('Total Liters ', round(tot_cnt * constant, 2))
            print('Time ', round((time.time() - time_zero)/60, 2), '\t',
                  time.asctime(time.localtime(time.time())), '\n')
        if id != 0:
            vol = round(tot_cnt * constant, 3)
            cost = round(vol * costPerCl, 3)
            df_events = df_events.append({'ID': id, 'Time' : time.asctime(time.localtime(start_time)), 'Volume': vol, 'Cost': cost}, ignore_index = True)
            df_users.loc[df_users['ID'] == id, 'Charge'] -= cost

    
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