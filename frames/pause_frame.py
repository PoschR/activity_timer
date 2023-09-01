import os
import tkinter as tk
from datetime import datetime
from datetime import timedelta

from util.rotating_light import RotatingLight
from util.spotlight import SpotLight
from util.stop_watch import StopWatch


class PauseFrame(tk.Frame, SpotLight):
    def __init__(self, parent_frame: tk.Frame, rotating_lights: RotatingLight, notes_dir: str):
        super().__init__(parent_frame, bg="black", width=100, height=100)

        self.notes_dir = notes_dir

        self.task_watch = StopWatch()
        self.pause_label = tk.Label(self, text="Start activity. Time is running!", font="Times 64",
                                    bg="black", fg="white")

        self.clock_label = tk.Label(self, text="00:00:00", font="Times 186",
                                    bg="black", fg="white")

        self.pause_edit = tk.Text(self, bg="black", fg="white", font=("Helvetica", 22),
                                  insertbackground="white")

        self.finish_pause_button = tk.Button(self,
                                             text="Finish Activity",
                                             command=rotating_lights.next_light,
                                             bg="black")

        self.visible = False

    def light_on_me(self):
        self.pause_label.pack(expand=True)
        self.clock_label.pack(expand=True)
        self.pause_edit.pack()
        self.finish_pause_button.pack()
        self.grid(row=0, column=0, sticky="nsew")

        self.winfo_toplevel().attributes('-fullscreen', True)

        self.task_watch.start()
        self.visible = True
        self.display_timer()

    def light_leaves_me(self):
        edit_text = self.pause_edit.get("1.0", "end-1c")

        if edit_text != "":
            now = datetime.now()
            full_iso_string = now.isoformat()
            split_iso = full_iso_string.split("T")
            iso_date = split_iso[0]
            iso_time = split_iso[1]

            thought_file_name = iso_date + ".md"
            thoughts_file_addr = os.path.join(self.notes_dir, thought_file_name)
            with open(thoughts_file_addr, "a") as thought_file:
                if os.path.getsize(thoughts_file_addr) == 0:
                    thought_file.write("## " + iso_time + "\n")
                else:
                    thought_file.write("\n## " + iso_time + "\n")
                thought_file.write(edit_text)

            self.pause_edit.delete(1.0, "end-1c")
        self.winfo_toplevel().attributes('-fullscreen', False)

        self.pause_label.pack_forget()
        self.clock_label.pack_forget()
        self.pause_edit.pack_forget()
        self.finish_pause_button.pack_forget()

        self.grid_remove()
        self.visible = False

    def display_timer(self) -> None:
        if self.visible:
            current_delta = timedelta(seconds=self.task_watch.elapsed())
            timer_tick = (datetime(1, 1, 1) + current_delta).strftime("%H:%M:%S")
            hundreds = str(int(current_delta.microseconds / 10000)).zfill(2)
            timer_tick += "."+hundreds
            self.clock_label.configure(text=timer_tick)
            self.clock_label.after(10, self.display_timer)
