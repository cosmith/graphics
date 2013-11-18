from PIL import Image
from random import randint
from vector import Vec
import math

SIZE = (500, 500)


class Plane(Vec):
    """
    A plane is just a normal vector
    """
    def __init__(self, x, y, z):
        return super(Plane, self).__init__(x, y, z)


class Camera:

    def __init__(self, position, direction, image):
        """
        """
        self.position = position
        self.direction = direction / direction.length()
        self.eye = self.position + self.direction
        self.subdivision = []

        self.image = image
        self.width, self.height = image.size

        self.SUB_COUNT = 10


    def __repr__(self):
        return("%s %s %s" % (self.position, self.direction, [x for x in dir(self) if x[0] != '_']))


    def capture(self):
        self.subdivide()

        for x in range(self.width):
            for y in range(self.height):
                pixel = self.pixel(x, y)
                self.image.putpixel((x, y), pixel)


    def subdivide(self):
        self.subdivision = []

        center = self.eye + self.direction * 2

        # vector defining the plane
        plane1 = Vec(-self.direction.y / self.direction.x, 1, 0)
        plane2 = Vec(-self.direction.z / self.direction.x, 0, 1)

        plane1 /= plane1.length()
        plane2 /= plane2.length()

        r = range(-self.SUB_COUNT/2, self.SUB_COUNT/2)
        for x in r:
            for y in r:
                # the position on the plane
                pos = center + (plane1 * x) + (plane2 * y)
                # the vector pointing to the point on the grid
                res = pos - self.eye

                self.subdivision.append(res)


    def pixel(self, x, y):
        """
        Get a pixel color
        """
        # find the appropriate subdivision cell
        # and get the color associated with it
        ix = int(float(x) / self.width * self.SUB_COUNT)
        iy = int(float(y) / self.height * self.SUB_COUNT)
        index = self.SUB_COUNT * ix + iy

        return self.trace(self.subdivision[index])

    def trace(self, vec):
        """
        Send a ray to infinity!
        """
        g = int(vec.dot(self.direction) * 100)
        # if randint(0, 100) > 99: print g
        return (g, g, g)


canvas = Image.new("RGB", SIZE)

c = Camera(Vec(0, 0, 0), Vec(1, 1, 1), canvas)
c.capture()



canvas.show()