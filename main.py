from gpiozero import DistanceSensor  # Import the DistanceSensor class from the gpiozero library
from time import sleep  # Import the sleep function from the time module for delay
from acc_script import read_MPU_data 
import requests as req
import os

# Initialize the ultrasonic sensor
sensor = DistanceSensor(echo=24, trigger=23)


server_ip_address=os.environ["SERVER_IP_ADDRESS"]


def measure_distance() -> int:

   distance = int(sensor.distance * 100)  # Measure the distance and convert it to an integer

   #distance_label.config(text="Distance: {} cm".format(distance))  # Update the distance label with the new distance
   print(f"distance: {distance}")
   
   return distance
       

       
while True:
   giro_data=read_MPU_data()
   distance_data=measure_distance()
   sound_name=""
   
   if abs(giro_data["giro_x"]) > 10 or abs(giro_data["giro_y"]) > 10 or abs(giro_data["giro_z"]) > 10:
          # ignore the distance data
          sound_name="picked_up_sound"
   elif distance_data < 10:
          # the train smashed into something
          sound_name="hurt_sound"
   else:
          # make chuu chuu sounds
          sound_name="moving_sound"
          
       
   try:
          response=req.get(f"http://{server_ip_address}:5000/play/train_sounds?filename={sound_name}")
          print(response)
   except ConnectionRefusedError as err:
          print(f"an error occured while making the call: {err}")
       
   sleep(0.1)
