from math import cos, radians, sin

class Car:
    """
    Arg
    Parse
    """
    def __init__(self, x = 0.0, y = 0.0, heading = 0.0):
        self.x = x
        self.y = y
        self.heading = heading
    def turn(self, degrees):
        """
        Tells the degrees and the turning radius for the car object
        """
        self.degrees = degrees
        self.heading = (self.heading + self.degrees) % 360
        print(self.degrees)
        
    def drive(self, distance):
        """
        Solves for where the car will go and the distance to the destination
        """
        self.x += sin(radians(distance)) * self.heading
        self.y -= cos(radians(distance)) * self.heading
    
def sanity_check():
    # return value of car object
    carRun = Car()
    carRun.heading = 90
    carRun.x = 10
