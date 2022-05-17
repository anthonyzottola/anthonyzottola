from InitialSetup import * #importing the initial setup
from CubeFunctions import * #importing cubefunctions since some rail functions depend on the cube functions

#gets requested cube color value: 1 => Red, 2 => Blue, 3 => Green
#checks if RailArr has a cube of that color still in it,
#if it does moves rail to the cube, slaps it off to delivery area,
#and updates RailArr to have 0 in that slot. returns updated RailArr

#Setup routine to store which cube colors are on the rail, 
#and where the colors are. returns RailArr
def CubePositionOnRailRoutine():
  i = 0 #Helps control the range of the for loop
  RailArr = [] #Emtpy array
  for i in range(6): #does this routine to get all 6 values
    print("requested slot in sort: " + str(i))
    moveRailUSRough(i) #moves to the next slot (positive direction)
    time.sleep(1) #waits until we get there
    UC = FindUnknownCube() #Gets the requested color's UC
    RailArr.append(UC) #Append it to the RailArr in order to get a single number to represent a color
    
    #Just print statements for helping us test if the rail color sensors gives us the right color 
    if UC == 1: 
      print("Cube " + str(i + 1) + " is Red")
    elif UC == 2:
      print("Cube " + str(i + 1) + " is Green")
    elif UC == 3:
      print("Cube " + str(i + 1) + " is Blue")
    elif UC == 4:
      print("Cube " + str(i + 1) + " is Yellow")
    elif UC == 5:
      print("Cube " + str(i + 1) + " is Orange")
    elif UC == 6:
      print("Cube " + str(i + 1) + " is Purple")
    else:
      print("Cube cannot be detected")
  return RailArr #Returns the newly updated RailArr after every for in range loop

#Method to help us get a good idea of where the current position is on the rail
#It uses a dictionary of tested values of where the slots should be when using the ultrasonic
#sensor. This should return its slot value as a numerical index
def ultrasensorCurrentPos():
    d_SlotsDistances = {0: (50,21.5), #Measured values range of RailArr position 0. (50 is overkill, 25 works fine)
                        1: (21.49,18.5), #Measured values range of RailArr position 1
                        2: (18.49,13.7), #Measured values range of RailArr position 2
                        3: (13.69,10.3), #Measured values range of RailArr position 3
                        4: (10.29,5.49), #Measured values range of RailArr position 4
                        5: (5.48,0)} #Measured values range of RailArr position 5
    CurrentRailPosition = 0 #Sets current position as blank variable
    RailDistance = UltraSensor.get_cm() #Gets the current US position in cm
    print("Rail dis: " + str(RailDistance))
    for positionkey in d_SlotsDistances: #Checks where our requested value is in the dictionary
        time.sleep(0.05)
        if  d_SlotsDistances[positionkey][0] >= RailDistance and RailDistance >= d_SlotsDistances[positionkey][1]: #Gets us the key 
            #of the dictionary values we are inbetween
            CurrentRailPosition = positionkey #Sets the key as the current rail position
            print(CurrentRailPosition)
            break
    return CurrentRailPosition #Returns the newly updated rail position

#Helps us get a rough idea of the current ultrasonic rail postion
#Reliable but not reliable enough to not have a moveRailUSPrecise function called after
def moveRailUSRough(locIndex):
  power = 20 #initial power of the rail is 20
  initialUSSlot = ultrasensorCurrentPos() #Getting rail position
  print("movement request initial slot: " + str(initialUSSlot))
  if initialUSSlot == locIndex: 
      moveRailUSPrecise(locIndex)
  elif locIndex == 0: #We use hardware to stop at the requested slot 0, (Could use US but this uses stoppers built in the hardware)
      RailMotor.set_power(-30) #Puts the motor at a faster speed in the negative direction
      time.sleep(2.8) #Overkill motor time but always enough time to stop at rail position 0
      RailMotor.set_power(0) #Stops the motor
      #No need to use the precise function since we know with our overkill motor and time, we are definitely at position 0
  elif locIndex == 5: #We use hardware to stop at the requested slot 5, (Could use US but this uses stoppers built in the hardware)
      RailMotor.set_power(30) #Puts the motor at a faster speed in the positive direction
      time.sleep(2.8) #Overkill motor time but always enough time to stop at rail position 5
      RailMotor.set_power(0) #Stops the motor
      #No need to use the precise function since we know with our overkill motor and time, we are definitely at position 5
  elif initialUSSlot < locIndex: #If we have our current slot at a smaller position than our requested slot
      RailMotor.set_power(power) #Set the motor in the positive direction
      while ultrasensorCurrentPos() < locIndex: #Poll until we get the 2 slot positions to match
          time.sleep(0.05) #Polls every 0.05 seconds
      print("finished pos movement")
      RailMotor.set_power(0) #Stops the motor
      time.sleep(0.2)
      moveRailUSPrecise(locIndex)  #Calls the precise ultrasonic function to correct any errors that may have occured
  elif initialUSSlot > locIndex: #If we have our current slot at a farther position than our requested slot
      RailMotor.set_power(-power) #Reverse the motor
      while ultrasensorCurrentPos() > locIndex: #Poll until we get the 2 slot positions to match
          time.sleep(0.05) #Polls every 0.05 seconds
      print("finished neg movement")
      RailMotor.set_power(0) #Stop the motor
      time.sleep(0.2) 
      moveRailUSPrecise(locIndex) #Calls the precise ultrasonic function to correct any errors that may have occured
      
    #Gets the current average rail distance
    #This helps us get a good idea of what the sensor is detecting and 
    #allows us to get rid of outliers by averaging the 8 last readings
    #incase one of the readings suddenly reads itself out of position
def getRailDistance():
    count = 0 #initial count 
    RailDistance = 0 #initial sum of RailDistance
    for i in range(8): #Runs the loop 8 times
        reading = UltraSensor.get_cm() #Gets the current postion
        if reading is not None and reading > 0 and reading < 40: #Making sure the reading is within our robots feasible range
            RailDistance += reading #Adds it to the RailDistance variable (Sum part of Sum/Count for an average)
            count += 1 #Adds it to the count variable (Count part of Sum/Count for an average)
        time.sleep(0.1) #Delay between readings
    return RailDistance/count #Returns the average current position reading


#Method that gives us an even more precise idea of our cube location
#This helps us know if the first moveRailUSRough was accurate or not
#and also helps us get the perfect lineup so that our hitter motor doesn't 
#accidently hit anything other than the cube (before it would hit the rails or miss the cube)
def moveRailUSPrecise(locIndex): 
    d_SlotCenters = {0: (30, 23), #Dictionary of tiny ranges for each rail slot 
                      1: (20.5, 19.2), #for the cube hitter motor to never miss
                      2: (16.7, 15.2),
                      3: (12.7, 10.7),
                      4: (8.2, 6.2),
                      5: (4.8, 0)}
    min = d_SlotCenters[locIndex][1] #Lower value of the each range
    max = d_SlotCenters[locIndex][0] #Higher value of each range
    railDistance = getRailDistance() #Gets the current rail distance
    print(railDistance)
    i = 0
    power = 14 #this value can be tuned before running
    while (max < railDistance or min > railDistance):#If outside our ranges, it corrects for it 
        if max < railDistance: #If under our max range, move the rail forwards
            RailMotor.set_power(power-i) #Gradually decrease the motors power
        else: #If below our max range, move the rail backwards
            RailMotor.set_power(-power+i) #Gradually increase the motors power
        time.sleep(0.5) #Updates to run this function every 0.5 seconds
        RailMotor.set_power(0) #Sets the motor to 0 once we get within the desired range
        railDistance = getRailDistance() #Get the new updated current position to run through this function again
        print(railDistance)
        i += 1 #This is how we control the motors gradually increase or decrease the motors power
        if i >=6: #Limits the motors eventual power to 6 off from starting if necessary
            i = 6
    print("done movement")
    return #Get out of function when we get within desired range
            
#Method to actually call the motor to hit the cube into the delivery area when called
def makeDelivery(RailArr): 
  requestedColor = getRequestedColor() #Gets the requested color from the getRequestedColor function
  #no cube presented
  if requestedColor == 0 or requestedColor == None: #Catches any request errors from request color sensor
    print("error getting requested cube color")
    return RailArr #Just brings back the RailArr without modifying
  print("requested color value: " + str(requestedColor))
  if RailArr.count(requestedColor) > 0: #Tells us if there even cubes present on the RailArr of the requested color
      locOfCubeToGet = ClosestCube(RailArr, requestedColor) #If so, we get the closest cube position that matches that description
  else: #If no cubes present, return to initial waiting for delivery request state
      print("No cubes of that color are in the Rail")
      return RailArr
  moveRailUSRough(locOfCubeToGet) #Move roughly to around the position of the corrected cube
  time.sleep(0.2) #Wait until we are aligned correct 
  cubeslap() #Slap the cube into the delivery area
  RailArr[locOfCubeToGet] = 0 #Setting the cube we just hit to a 0 in the array to let us know it isn't on the rail anymore
  return RailArr #Updates with the new RailArr

#Main robot state, waits for touch sensor press
#then makes a delivery of the requested cube
#takes initial RailArr and keeps RailArr updated
def deliveryMode(RailArr):
  while True:
      try:
        if StartTouch.is_pressed(): #Starts the if statement that makes deliveries multiple times
            print("delivery mode sensor touched") 
            RailArr = makeDelivery(RailArr) #Calls the makeDelivery function with RailArr and then updates 
            #the RailArr except with the UC value of the cube just delivered as 0
            time.sleep(1)
            while StartTouch.is_pressed(): #Helps us catch if the touch sensor is bugging out
                print("still pressed")
                time.sleep(0.1)
      except BaseException as ex:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
          print("delivery mode exception")
          print(ex)
          exit()

#Initial robot state, waits for touch sensor press to 
#start the cube position on rail routine, then returns 
#the resulting RailArr
def storeSetup():
  print("Robot waiting for cubes to be loaded on rail\n")
  print("Please press the delivery area touch sensor when the")
  print("cubes are on the rail and the rail is in position")
  
  while True:
    if StartTouch.is_pressed(): #When the touch sensor is pressed it starts the if statement
      print("Started initial Cube position on rail routine, please wait until completion")

      RailArr = CubePositionOnRailRoutine() #Starts the CubePositionOnRailRoutine() to get the 6 unknown cubes 
      #as an array of UCs which we know the values for
      print(RailArr)
      return RailArr

#Function to help us determine which cube would make the delivery faster
#Only useful when there are multiple cubes of the same color
#This helps the robot know what cube it is closer to if they are the same color
def ClosestCube(RailArr, requestedColor):
    CurrentUSPos = ultrasensorCurrentPos()  #Gets the current ultrasonic rail value and sets it as CurrentUSPos
    BeforeRailArr = (RailArr[:CurrentUSPos][::-1]) #Makes a separate array of just the values before the current position and flips it
    MiddleRailArr = [RailArr[CurrentUSPos]] #Makes a separate array of just the value of the current position
    AfterRailArr = RailArr[(CurrentUSPos+1):] #Makes a separate array of just the values after the current position
    # Example would be: RailArr = [1,5,4,6,2,3] 
    # CurrentUSPos = 3 (position 3 in array is current rail position)
    # BeforeRailArr = [4,5,1]
    # MiddleRailArr = [6]
    # AfterRailArr = [2,3]
    # BeforeRailArr is flipped so when we search, it searches for the closest values to our current position
    # [1,5,4,<====6====>2,3] 
    try: #Catches if there is a cube present on the current rail position that matches our requested cube
      if MiddleRailArr.index(requestedColor) == 0:
        return CurrentUSPos
        print("right on cube")
    except ValueError: #If not present, move into the for loop to check around
      pass  # do nothing!
    i = 0 #Helps us control the range of the searching
    for i in range(6): #We have to set the range to 6 to make sure it always checks every possible array value
            try:
                if BeforeRailArr.index(requestedColor) == i: #Check if the BeforeRailArr matches our current requested color
                    print("move " + str(i+1) + " to left")
                    return CurrentUSPos-i-1 #If it matches tell the robot the closest postion on the left side
            except ValueError:
                pass  # do nothing!
            try: 
                if AfterRailArr.index(requestedColor) == i: #Check if the AfterRailArr matches our current requested color
                    print("move " + str(i+1) + " to right")
                    return CurrentUSPos+i+1 #If it matches tell the robot the closest postion on the right side
            except ValueError:
                pass  # do nothing!




