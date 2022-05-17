from utils.brick import wait_ready_sensors, EV3ColorSensor, Motor, TouchSensor, EV3UltrasonicSensor, configure_ports
import time

StartTouch = TouchSensor(1) # port S1
UltraSensor = EV3UltrasonicSensor(2) # port S2
RequestColor = EV3ColorSensor(4) # port S3; color sensor to detect cube in delivery area
RailColor = EV3ColorSensor(3) # port S4; color sensor to detect cube color on rail

motorHIT = Motor("A") #port A; motor to knock cube off rail
RailMotor = Motor("B") #port B; motor to move rail
motorHIT.set_limits(power=35) #Setting the hitting motor to 35 power to limit its position change
RailMotor.set_limits(power=30) #Setting the rail motor to 30 power to limit its position change
