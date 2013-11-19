from PIL import Image
from random import randint
from vector import Vec
import math

SIZE = (200, 200)


class Scene:
    def __init__(self):
        self.objects = []

    def addobject(self, obj):
        if not isinstance(obj, SceneObject):
            raise TypeError()

        self.objects.append(obj)


class SceneObject:
    def __init__(self):
        pass

    def distance(self, point, ray):
        """
        Return the distance between the object and the point
        if following the vector ray
        Return None if no intersection
        """
        pass


class Plane(SceneObject):
    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal
        self.color = color

    def distance(self, point, ray):
        nv = self.normal.dot(ray)
        if nv <= 0:
            return None

        # we hit the plane
        return abs(self.normal.dot(point - self.point) / nv)


class Sphere(SceneObject):
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def distance(self, point, ray):
        pc = self.center - point # point to center vec
        pc_ray = math.acos((pc/pc.length()).dot(ray)) # angle between ray and PC
        max_angle = math.atan(self.radius / pc.length())

        if pc_ray > max_angle:
            return None

        return 100.0


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
                # normalize
                res /= res.length()

                self.subdivision.append(self.trace(res))


    def trace(self, ray):
        """
        Send a ray to infinity!
        """
        closest = 100000
        picked_color = (170, 220, 240) # sky

        for obj in self.scene.objects:
            dist = obj.distance(self.position, ray)
            if dist and dist < closest:
                closest = dist
                picked_color = self.normalize(obj.color, dist / 100)

        # sky
        return picked_color


    def normalize(self, color, g):
        if g == 0: # problem
            return (randint(0,255), randint(0,255), randint(0,255))

        return (abs(int(color[0]/g)), abs(int(color[1]/g)), abs(int(color[2]/g)))


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

plane1 = Plane(Vec(0, 0, 1), Vec(0, 0, 1), (40, 100, 50))
plane2 = Plane(Vec(100, 100, 10), Vec(0.4, 3, 5), (100, 50, 40))
sphere1 = Sphere(Vec(5, 5, 20), 1, (10, 200, 10))
sphere2 = Sphere(Vec(10, 20, 19), 1, (100, 20, 10))

scene.addobject(plane1)
# scene.addobject(plane2)
scene.addobject(sphere1)
scene.addobject(sphere2)

c = Camera(scene, Vec(0, 0, 20), Vec(1, 1, 0), canvas)
c.capture()

canvas.show()