import itertools


class RotatingLight:
    def __init__(self, list_of_rotations):
        self.list_of_rotations = list_of_rotations
        self.lights_cycle = itertools.cycle(self.list_of_rotations)
        self.current_lights = None

    def append_lights(self, list_of_lights):
        self.list_of_rotations.append(list_of_lights)

    def next_light(self):
        if self.current_lights is not None:
            for light in self.current_lights:
                light.light_leaves_me()

        self.current_lights = next(self.lights_cycle)

        for light in self.current_lights:
            light.light_on_me()