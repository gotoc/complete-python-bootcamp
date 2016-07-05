
# 1 - Fill in the Line class methods to accept coordinate as a pair of tuples and return the slope and distance of the line.

class Line(object):

    def __init__(self,coordinate1,coordinate2):
        # unpack the tuples
        self.x1,self.y1 = coordinate1
        self.x2,self.y2 = coordinate2

    def __str__(self):
        return "A line is a straight one-dimensional figure having no thickness and extending in both directions."

    def distance(self):
        # Yes, I had to look up the Pythagorean theorem to figure this out.
        return ((self.x2-self.x1)**2 + (self.y2-self.y1)**2)**.5

    def slope(self):
        return float((self.y2 - self.y1)) / (self.x2 - self.x1)

# Example functioning
coordinate1 = (3,2)
coordinate2 = (8,10)
li = Line(coordinate1,coordinate2)
print li
print "Distance of line is: ",li.distance()
print "Slope of line is: ",li.slope()

print "\n----------------------\n"

# 2 - Fill in the class
class Cylinder(object):

    pi = 3.14

    def __init__(self,height=1,radius=1):
        self.h = height
        self.r = radius

    def __str__(self):
        return "A cylinder is the surface formed by the points at a fixed distance from a given straight line called the axis of the cylinder."

    def volume(self):
        return self.pi * self.r**2 * self.h

    def surface_area(self):
        return 2 * self.pi * self.r * (self.r + self.h)

# Example functioning
c = Cylinder(2,3)
print c
print "Volume of cylinder is: ",c.volume()
print "Surface area is: ",c.surface_area()
