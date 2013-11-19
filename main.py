from PIL import Image
from random import randint
from vector import Vec
import math

SIZE = (640, 480)


class Scene():

    def __init__(self):
        self.planes = []

    def addplane(self, position, normal, color):
        self.planes.append((position, normal, color))


class Camera:

    def __init__(self, scene, position, direction, image):
        """
        """
        self.scene = scene

        self.position = position
        self.direction = direction / direction.length()
        self.subdivision = []

        self.image = image
        self.width, self.height = image.size

        self.SUB_COUNT = 100


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

        center = self.direction

        # vector defining the plane
        plane1 = Vec(-self.direction.y / self.direction.x, 1, 0)
        plane2 = Vec(-self.direction.z / self.direction.x, 0, 1)

        plane1 /= plane1.length()
        plane2 /= plane2.length()

        r = range(-self.SUB_COUNT/2, self.SUB_COUNT/2)
        size = float(self.SUB_COUNT)
        for x in r:
            for y in r:
                # the position on the plane
                pos = ((plane1 * x) + (plane2 * y)) / size
                # the vector pointing to the point on the grid
                res = center + pos

                self.subdivision.append(self.trace(res))


    def trace(self, vec):
        """
        Send a ray to infinity!
        """
        for position, normal, color in self.scene.planes:
            if normal.dot(vec) > 0:
                # we hit a plane
                g = normal.dot(vec) * 10
                return self.normalize(color, g)
            else:
                # sky
                return (170, 220, 240)


    def normalize(self, color, g):
        return (abs(int(color[0]*g)), abs(int(color[1]*g)), abs(int(color[2]*g)))

    def pixel(self, x, y):
        """
        Get a pixel color
        """
        # find the appropriate subdivision cell
        # and get the color associated with it
        ix = int(float(x) / self.width * self.SUB_COUNT)
        iy = int(float(y) / self.height * self.SUB_COUNT)
        index = self.SUB_COUNT * ix + iy

        return self.subdivision[index]




canvas = Image.new("RGB", SIZE)

scene = Scene()
scene.addplane(Vec(0, 0, 0), Vec(0, 0, 1), (40, 100, 50))

c = Camera(scene, Vec(0, 0, 20), Vec(1, 1, 0), canvas)
c.capture()



canvas.show()