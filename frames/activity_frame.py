import tkinter as tk
from typing import Any

from util.geometric_timer import GeometricTimer
from util.spotlight import SpotLight
from util.stop_watch import StopWatch


def setup_grid_row(widgets_to_add, at_row: int, with_padx: int, with_pady: int):
    for i in range(0, len(widgets_to_add)):
        widgets_to_add[i].grid(row=at_row, column=i, padx=with_padx, pady=with_pady)


class ActivityFrame(tk.Frame, SpotLight):
    def __init__(self, parent_frame: tk.Frame, activity_timer: GeometricTimer, config: dict[str, Any]):
        super().__init__(parent_frame,  width=100, height=100)

        self.activity_timer = activity_timer
        self.activity_timer.add_second_reaction(self.decrease_time)

        self.text_frame = tk.Frame(self, width=100, height=30)
        self.timer_frame = tk.Frame(self, width=100, height=30)

        self.countdown = 0
        self.countdown_watch = StopWatch()

        self.entered_text = ""

        self.var_seconds = tk.IntVar(value=config["default_seconds"])
        self.var_minutes = tk.IntVar(value=config["default_minutes"])
        self.var_hours = tk.IntVar(value=config["default_hours"])
        self.var_timed = tk.BooleanVar(value=config["default_timed"])
        self.var_task_name = tk.StringVar()

        self.time_label = tk.Label(self.text_frame, text="Enter Activity:")

        self.start_button = tk.Button(self.timer_frame, text="Start", command=self.start_countdown)
        self.task_row = [
            tk.Label(self.timer_frame,
                     text="Descr"),
            tk.Entry(self.timer_frame,
                     textvariable=self.var_task_name,
                     validate='key',
                     validatecommand=(self.register(self.check_startable), '%P')),
            tk.Label(self.timer_frame,
                     text="In"),
            tk.Spinbox(self.timer_frame,
                       from_=0, to=23,
                       increment=1,
                       textvariable=self.var_hours,
                       wrap=True, width=3),
            tk.Label(self.timer_frame,
                     text="h"),
            tk.Spinbox(self.timer_frame,
                       from_=0, to=59,
                       increment=1,
                       textvariable=self.var_minutes,
                       wrap=True, width=3),
            tk.Label(self.timer_frame,
                     text="m"),
            tk.Spinbox(self.timer_frame,
                       from_=0, to=59,
                       increment=1,
                       textvariable=self.var_seconds,
                       wrap=True, width=3),
            tk.Label(self.timer_frame,
                     text="s"),
            tk.Checkbutton(self.timer_frame,
                           text="Measure Activity Time?",
                           variable=self.var_timed),
            self.start_button
        ]

    def start_countdown(self):
        chosen_seconds = int(self.var_seconds.get())
        chosen_minutes = int(self.var_minutes.get())
        chosen_hours = int(self.var_hours.get())
        self.countdown = chosen_hours * 3600 + chosen_minutes * 60 + chosen_seconds

        for task_row_widget in self.task_row:
            task_row_widget.config(state="disabled")
        self.start_button.config(state="disabled")

        self.activity_timer.start_timers(self.countdown)

    def light_on_me(self):
        self.time_label.pack(side="left")

        setup_grid_row(self.task_row, at_row=0, with_padx=1, with_pady=2)

        self.text_frame.pack(padx=10, pady=2, fill=tk.BOTH)
        self.timer_frame.pack(padx=10, pady=2, expand=True, fill=tk.BOTH)

        self.grid(row=0, column=0)

        for task_row_widget in self.task_row:
            task_row_widget.config(state="normal")

        self.update_button()

    def light_leaves_me(self):
        self.grid_remove()

        self.timer_frame.pack_forget()
        self.text_frame.pack_forget()

        for task_row_widget in self.task_row:
            task_row_widget.grid_remove()

        self.time_label.pack_forget()

    def decrease_time(self):
        elapsed_time = int(self.activity_timer.elapsed_time())
        remainder = max(0, self.countdown - elapsed_time)

        self.var_seconds.set(remainder % 60)
        self.var_minutes.set(remainder // 60)
        self.var_hours.set(remainder // 3600)

    def check_startable(self, entered_text):
        self.entered_text = entered_text
        self.update_button()

        return True

    def update_button(self):
        if self.entered_text != "":
            self.start_button.config(state="normal")
        else:
            self.start_button.config(state="disabled")
