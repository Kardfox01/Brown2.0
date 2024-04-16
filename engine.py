from particle import Particle
from time import sleep, time

import parameters as ps
import numpy as np


class Engine:
    def __init__(self):
        self.__particles: list[Particle] = []
        self.__pause = False

        self.k = 1


    def act(self, screen, draw):
        w, h = screen.get_size()
        for particle in self.__particles:
            if (
                particle.position[0] - particle.radius < 0        and particle.velocity[0] < 0 or
                particle.position[0] + particle.radius > w and particle.velocity[0] > 0
            ):
                particle.velocity[0] *= -1
                particle.collided = True

            if (
                particle.position[1] - particle.radius < 0         and particle.velocity[1] < 0 or
                particle.position[1] + particle.radius > h and particle.velocity[1] > 0
            ):
                particle.velocity[1] *= -1
                particle.collided = True

            if not particle.collided and not self.__pause:
                for another in self.__particles:
                    diff = particle.position - another.position

                    if not (
                        diff[0]**2 + diff[1]**2 < particle.radius**2 + 2*particle.radius*another.radius + another.radius**2 and
                        particle.uid != another.uid
                    ): continue

                    m1, v1, p1 = particle.mass, particle.velocity, particle.position
                    m2, v2, p2 = another.mass,  another.velocity, another.position

                    square_norm = diff[0]**2 + diff[1]**2
                    if square_norm <= 0:
                        continue

                    M = m1 + m2

                    particle.velocity = self.k * (v1 - 2*m2 / M * np.dot(v1 - v2, p1 - p2) / square_norm * (p1 - p2))
                    another.velocity  = self.k * (v2 - 2*m1 / M * np.dot(v2 - v1, p2 - p1) / square_norm * (p2 - p1))

                    norm = np.sqrt(square_norm)
                    direction = (particle.position - another.position) / norm
                    shift = direction * (particle.radius + another.radius - norm)

                    particle.position += shift
                    another.position  -= shift

                    another.collided = True

            if not self.__pause and not particle.collided:
                particle.position += particle.velocity

            if particle.trajectory:
                for start, end, color in particle.trajectory:
                    draw.line(
                        screen,
                        color,
                        start,
                        end,
                        4
                    )

                draw.circle(
                    screen,
                    (0, 255, 0),
                    particle.trajectory[0][0],
                    5
                )

            if particle.show:
                draw.circle(
                    screen,
                    particle.color,
                    particle.position,
                    particle.radius
                )

            particle.collided = False


    def create(self, particle: Particle):
        self.__particles.append(particle)


    def highlight(self, uid: int):
        if uid > self.count: raise IndexError

        for particle in self.__particles:
            if particle.uid != uid:
                particle.show = False


    def track(self, seconds: int, uid: int):
        self.highlight(uid)
        self.__pause = False

        start = time()

        particle = self.__particles[uid]
        while time() - start < seconds:
            speed = np.sqrt(particle.velocity[0]**2 + particle.velocity[1]**2)

            color = (
                particle.color[0] * speed // ps.V // 2,
                particle.color[1] * speed // ps.V // 2,
                particle.color[2] * speed // ps.V // 2
            )

            start_position = tuple(particle.position)
            sleep(.07)

            particle.trajectory.append(
                (
                    start_position,
                    tuple(particle.position),
                    (
                        color[0] if color[0] <= 255 else 255,
                        color[1] if color[1] <= 255 else 255,
                        color[2] if color[2] <= 255 else 255
                    )
                ) #type: ignore
            )


    def reset(self):
        for particle in self.__particles:
            particle.show = True
            particle.trajectory.clear()
        self.__pause = False
        self.k = 1


    def collapse(self):
        self.__particles.clear()


    def pause(self):
        self.__pause = not self.__pause


    @property
    def count(self):
        return len(self.__particles)

