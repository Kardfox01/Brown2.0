from parameters import RADIUS, MASS, COLOR
from numpy import array, sqrt


class Particle:
    def __init__(
        self,
        uid   : int,
        xy    : tuple[int, int],
        dxdy  : tuple[int, int],
        radius: int                  = RADIUS,
        m     : int                  = MASS,
        color : tuple[int, int, int] = COLOR,
        show  : bool                 = True
    ):
        self.uid        = uid
        self.position   = array(xy, dtype="float64")
        self.velocity   = array(dxdy, dtype="float64")
        self.radius     = radius
        self.mass       = m
        self.color      = color
        self.show       = show
        self.collided   = False
        self.trajectory = []
