from threading import Timer

from util.stop_watch import StopWatch


def trigger_all(reactions):
    for reaction in reactions:
        reaction()


class GeometricTimer:
    def __init__(self, denominator: int):
        self.denominator = denominator
        self.seconds_timer = None
        self.total_timer = None
        self.total_time = 0
        self.total_watch = StopWatch()
        self.seconds_reactions = []
        self.division_reactions = []
        self.total_time_reactions = []

    def __del__(self):
        if self.seconds_timer is not None:
            self.seconds_timer.cancel()
        if self.total_timer is not None:
            self.total_timer.cancel()

    def start_timers(self, time: float):
        self.total_watch.reset()
        self._start_timers(time)

    def _start_timers(self, time: float):
        self.total_time = time / 2
        self.seconds_timer = Timer(1, self.lap_second)
        self.total_timer = Timer(self.total_time, self.divide_total_time)
        self.seconds_timer.start()
        self.total_timer.start()
        self.total_watch.start()

    def lap_second(self):
        trigger_all(self.seconds_reactions)

        if self.total_time > 1:
            self.seconds_timer = Timer(1, self.lap_second)
            self.seconds_timer.start()

    def divide_total_time(self):
        self.total_watch.stop()

        # Max 2 seconds for reactions to complete
        self.seconds_timer.join(1)

        if self.total_time > 1:
            trigger_all(self.division_reactions)
            self._start_timers(self.total_time)
        else:
            trigger_all(self.total_time_reactions)

    def elapsed_time(self):
        return self.total_watch.elapsed()

    def add_second_reaction(self, reaction_fun):
        self.seconds_reactions.append(reaction_fun)

    def add_total_time_over_reaction(self, reaction_fun):
        self.total_time_reactions.append(reaction_fun)

    def add_blocking_divide_reaction(self, reaction_fun):
        self.division_reactions.append(reaction_fun)
