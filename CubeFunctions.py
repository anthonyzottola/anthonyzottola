from InitialSetup import * #importing the initial setup

#makeDelivery helper method to 'slap' cube off of the rail
#into the delivery zone once the rail is in the correct position
#return True if succesful, False otherwise
#WARNING: can cause BrickPi to crash if motor commands overlap
def cubeslap(): #The main cube function to "slap" the cube into the delivery area when called
  try:
    motorHIT.set_power(10) #Sets the motor a positive power to push the cube forward
    time.sleep(0.8) #Sleeping so the motor has enough time to hit
    motorHIT.set_power(-10) #Sets the motor a negative power to push the cube backwards
    time.sleep(0.8) #Sleeping so the motor has enough time to move back to its original spot
    motorHIT.set_power(0) #Stops the movement of the motor
  except:
    print("Error") #Returns false and prints Error if method doesn't work correct
    return False

#CubePositionOnRailRoutine helper method to get cube
#reading from the Rail and return it
#UC (Unknown Color) helps us by putting the cube
#color as 1 numerical value 
def FindUnknownCube(): 
    try:
        arr = RailColor.get_rgb() #Getting the rbg from the rail color sensor
        print(RailColor.get_rgb())
        x = int(arr[0]) #Setting the 0 position in the array as x
        y = int(arr[1]) #Setting the 1 position in the array as y
        z = int(arr[2]) #Setting the 2 position in the array as z
        if (x < 30 and y < 30 and z < 30): #If statement tell us if there is no cube present to scan
            print("No cube detected")
        elif (x < 5 and y < 5) or (x < 5 and z < 5) or (y < 5 and z < 5): #Sometimes the color sensor only returns 1 array
            print("Bad reading") #value so we used this neat trick to help us discard that given array
        else:
            if (x > 6*y and x > 6*z): #Unique X Y Z combination that only applies to red
                UC = 1 #UC 1 is a red cube
                print("Cube is Red")
                return UC
            elif (y > 4*x and y > 4*z): #Unique X Y Z combination that only applies to green
                UC = 2 #UC 2 is a green cube
                print("Cube is Green")
                return UC
            elif (z > 1.6*x): #Unique X Y Z combination that only applies to blue
                UC = 3 #UC 3 is a blue cube
                print("Cube is Blue")
                return UC
            elif (x > 10*z): #Unique X Y Z combination that only applies to yellow
                UC = 4 #UC 4 is a yellow cube
                print("Cube is Yellow")
                return UC
            elif (2.5*z > y > 1.5*z): #Unique X Y Z combination that only applies to orange
                UC = 5 #UC 5 is a orange cube
                print("Cube is Orange")
                return UC
            elif (2*y > x > y and 2*y > z > y): #Unique X Y Z combination that only applies to purple
                UC = 6 #UC 6 is a purple cube
                print("Cube is Purple")
                return UC
            else: #If the cube doesn't match any of these XYZ relationships, cube is faulty or couldn't scan right
                UC = 0
                return UC
    except:
        print("Error")

#gets cube rgb data from request area color sensor
#prints to console requested cube color and returns 
#the color value. UC (Unknown Color) helps us by putting the cube
#color as a numerical value 
def getRequestedColor():
  try:
    arr = RequestColor.get_rgb() #Getting the rbg from the request color sensor
    print("getRequestedColor get_rgb() val:")
    print(RequestColor.get_rgb())
    x = arr[0] #Setting the 0 position in the array as x
    y = arr[1] #Setting the 1 position in the array as y
    z = arr[2] #Setting the 2 position in the array as z
    if x is None or y is None or z is None or (x < 30 and y < 30 and z < 30): #If statement tell us if there is no cube present to scan
        print("No cube detected") #None was also added since the request sensor sometimes bugs out and gives us a None value
    elif (x < 5 and y < 5) or (x < 5 and z < 5) or (y < 5 and z < 5): #Sometimes the color sensor only returns 1 array
        print("Bad reading") #value so we used this neat trick to help us discard that given array
    else:
        if (x > 6*y and x > 6*z): #Unique X Y Z combination that only applies to red
            UC = 1 #UC 1 is a red cube
            print("Requested cube is Red")
            return UC 
        elif (y > 4*x and y > 4*z): #Unique X Y Z combination that only applies to green
            UC = 2 #UC 2 is a green cube
            print("Requested cube is Green")
            return UC
        elif (z > 1.6*x): #Unique X Y Z combination that only applies to blue
            UC = 3 #UC 1 is a blue cube
            print("Requested cube is Blue")
            return UC
        elif (x > 10*z): #Unique X Y Z combination that only applies to yellow
            UC = 4 #UC 4 is a yellow cube
            print("Requesed cube is Yellow")
            return UC
        elif (2.5*z > y > 1.5*z): #Unique X Y Z combination that only applies to orange
            UC = 5 #UC 5 is a orange cube
            print("Requested cube is Orange")
            return UC
        elif (2*y > x > y and 2*y > z > y): #Unique X Y Z combination that only applies to purple
            UC = 6 #UC 6 is a purple cube
            print("Requested cube is Purple")
            return UC
        else: #If the cube doesn't match any of these XYZ relationships, cube is faulty or couldn't scan right
            UC = 0
            return UC
  except:
    print("Request Cube Error")


