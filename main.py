from CubeFunctions import * #No need to import InitialSetup since it is already imported through 
from RailFunctions import * #both the cube and rail functions python files
            
if __name__ == "__main__":
    i = 0 #For use in for loops 
    wait_ready_sensors() #Waiting for the sensors to be ready before we start the main process
    print("sensors ready main")
    while True:
        try:
          #typical operation:
          print("Robot entering store setup mode") #Waiting for the touch sensor's initial touch
          RailArr = storeSetup() #Starts the setup that gives us our RailArr (Cube array)
          print("Robot entering delivery mode") #Waiting for touch sensor's second touch
          deliveryMode(RailArr) #Starts the delivery mode that uses the request color sensor to get us our requested cube
          
    
        except BaseException as ex:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
          print("main exception") #Prints main exception and causes the program to quit if error happens
          print(ex)
          exit()
          