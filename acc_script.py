#Include the library files
import RPi.GPIO as GPIO
import smbus 
from time import sleep

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Set the servo motor pin as output pin
GPIO.setup(4,GPIO.OUT)

pwm = GPIO.PWM(4,50)
pwm.start(0)

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
GYRO_XOUT  = 0x43
GYRO_YOUT  = 0x45
GYRO_ZOUT  = 0x47


bus = smbus.SMBus(1) # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68 # MPU6050 device address



def MPU_Init():
    
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
        
    #concatenate higher and lower value
    value = ((high << 8) | low)
            
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value
    

MPU_Init()

def read_MPU_data() -> dict:
    giro_data_dict={}
    #Read Accelerometer raw value
    try:
        acc_x = read_raw_data(ACCEL_XOUT)
        acc_y = read_raw_data(ACCEL_YOUT)
        acc_z = read_raw_data(ACCEL_ZOUT)
        
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0 
        Az = acc_z/16384.0
        
    except OSError as os_error:
        print(f"the acc stopped working: {os_error}. Restarting..")
        MPU_Init()

    #Read Gyroscope raw value
    try:
        gyro_x = read_raw_data(GYRO_XOUT)
        gyro_y = read_raw_data(GYRO_YOUT)
        gyro_z = read_raw_data(GYRO_ZOUT)
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        
        giro_data_dict["giro_x"]=Gx
        giro_data_dict["giro_y"]=Gy
        giro_data_dict["giro_z"]=Gz
    except OSError as os_error:
        print(f"the acc stopped working: {os_error}. Restarting..")
        MPU_Init()


    # Uncomment below line to see the Accelerometer and Gyroscope values   
    print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s")#, "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 
    
    if Ax == 0.0 and Ay == 0.0 and Az == 0.0:
        print(f"Restarting acc...")
        MPU_Init()
    
    return giro_data_dict
    
# while True:
    # da=read_MPU_data()
    # sleep(0.1)

        
