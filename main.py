from gpiozero import DistanceSensor  # Import the DistanceSensor class from the gpiozero library
import tkinter as tk  # Import the tkinter library for creating the GUI
from tkinter import font  # Import the font module from tkinter for customizing the font
from time import sleep  # Import the sleep function from the time module for delay
import pygame # for audio output

# Initialize the ultrasonic sensor

sensor = DistanceSensor(echo=24, trigger=23)

# Initialize the Tkinter window
window = tk.Tk()

# initialize player
pygame.mixer.init()

def measure_distance():

   distance = int(sensor.distance * 100)  # Measure the distance and convert it to an integer

   #distance_label.config(text="Distance: {} cm".format(distance))  # Update the distance label with the new distance
   print(distance)
   

   if distance < 5:
       # the train smashed into something
       sound_path=""

   else:
       # make chuu chuu sounds
       sound_path=""
           
   sound = pygame.mixer.Sound(sound_path)
   playing = sound.play()
   while playing.get_busy():
          pygame.time.delay(100)

       

   window.after(800, measure_distance)  # "delay"

   

# Start measuring distance
measure_distance()

# Run the Tkinter event loop
window.mainloop()
