from math import sin, cos, radians


# stores three points of the triangle
class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


def make_triangle(scale, internal_angle, rotation):
    # define the points in a unit space
    ia = (radians(internal_angle) * 2) - 1
    p1 = (0, -1)
    p2 = (cos(ia), sin(ia))
    p3 = (cos(ia) * -1, sin(ia))

    # rotate the points
    ra = radians(rotation)
    rp1x = p1[0] * cos(ra) - p1[1] * sin(ra)
    rp1y = p1[0] * sin(ra) + p1[1] * cos(ra)
    rp2x = p2[0] * cos(ra) - p2[1] * sin(ra)
    rp2y = p2[0] * sin(ra) + p2[1] * cos(ra)
    rp3x = p3[0] * cos(ra) - p3[1] * sin(ra)
    rp3y = p3[0] * sin(ra) + p3[1] * cos(ra)
    rp1 = (rp1x, rp1y)
    rp2 = (rp2x, rp2y)
    rp3 = (rp3x, rp3y)

    # scale the points
    sp1 = [rp1[0] * scale, rp1[1] * scale]
    sp2 = [rp2[0] * scale, rp2[1] * scale]
    sp3 = [rp3[0] * scale, rp3[1] * scale]

    return Triangle(sp1, sp2, sp3)


def offset_triangle(triangle, offset_x, offset_y):
    triangle.p1[0] += offset_x
    triangle.p1[1] += offset_y
    triangle.p2[0] += offset_x
    triangle.p2[1] += offset_y
    triangle.p3[0] += offset_x
    triangle.p3[1] += offset_y
    return triangle
