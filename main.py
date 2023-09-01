from functools import partial
from typing import Any

from pydub import AudioSegment
from pydub.playback import play

from frames.activity_frame import ActivityFrame
from frames.pause_frame import PauseFrame
from util.geometric_timer import GeometricTimer
from util.jukebox import JukeBox
from util.rotating_light import RotatingLight

import tkinter as tk

import argparse
import toml


def setup_container_frame():
    created_cont_frame = tk.Frame(master, width=100, height=100)
    created_cont_frame.pack(side="top", fill="both", expand=True)
    created_cont_frame.grid_rowconfigure(0, weight=1)
    created_cont_frame.grid_columnconfigure(0, weight=1)

    return created_cont_frame


def load_interlude_play(used_config: dict[str, Any]):
    interlude_sound = AudioSegment.from_wav(used_config["alarm_sound"])[:used_config["alarm_playback_ms"]]
    interlude_sound += used_config["alarm_db_increase"]

    return interlude_sound


def fetch_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-c", "--config", default="config.toml", help="TOML file for custom configurations.")
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = fetch_args()
    config = toml.load(args.config)

    master = tk.Tk()
    master.title(config["window_title"])

    container_frame = setup_container_frame()

    dividing_timer = GeometricTimer(config["timing_denominator"])

    # After a geometric round, sound alarm
    dividing_timer.add_blocking_divide_reaction(partial(play, load_interlude_play(config)))

    frame_rotation = RotatingLight([[ActivityFrame(container_frame, dividing_timer, config)]])

    frame_rotation.append_lights([
        PauseFrame(container_frame, frame_rotation, config["notes_dir"]),
        JukeBox(config["bg_song_list"], False)
    ])

    # When time is over, focus on the next screen
    dividing_timer.add_total_time_over_reaction(frame_rotation.next_light)

    # Activate first light, aka the activity frame
    frame_rotation.next_light()

    master.mainloop()
