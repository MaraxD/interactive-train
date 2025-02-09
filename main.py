from gpiozero import DistanceSensor  # Import the DistanceSensor class from the gpiozero library
from time import sleep  # Import the sleep function from the time module for delay
import pygame # for audio output
from acc_script import read_MPU_data 
import requests as req

# Initialize the ultrasonic sensor

sensor = DistanceSensor(echo=24, trigger=23)

# initialize player
pygame.mixer.init()

def measure_distance() -> int:

   distance = int(sensor.distance * 100)  # Measure the distance and convert it to an integer

   #distance_label.config(text="Distance: {} cm".format(distance))  # Update the distance label with the new distance
   print(f"distance: {distance}")
   
   return distance
       

       
while True:
   giro_data=read_MPU_data()
   distance_data=measure_distance()
   sound_name=""
   
   if distance_data < 5:
          # the train smashed into something
          sound_name=""

   else:
          # make chuu chuu sounds
          sound_name=""
          try:
              response=req.get(f"http://192.168.1.201:5000/play/{sound_name}")
              print(response.)
          except ConnectionRefusedError as err:
              print(f"an error occured while making the call: {err}")
       # sound = pygame.mixer.Sound(sound_path)
       # playing = sound.play()
       # while playing.get_busy():
              # pygame.time.delay(100)
   sleep(0.1)
