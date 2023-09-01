import random

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio, play

from util.spotlight import SpotLight


class JukeBox(SpotLight):
    def __init__(self, music_files: list[str], block_on_playback: False):
        self.block_on_playback = block_on_playback
        self.pause_sounds = []
        self.current_index = -1

        random_music_files = music_files.copy()
        random.shuffle(random_music_files)

        for sound in random_music_files:
            loaded_sound = AudioSegment.from_mp3(sound)
            down_duration = 5000
            gain_fade = -10
            loaded_sound = loaded_sound.fade(to_gain=gain_fade, duration=down_duration, start=10000) \
                .fade(from_gain=gain_fade, to_gain=gain_fade,
                      duration=len(loaded_sound) - down_duration, end=float('inf'))
            self.pause_sounds.append(loaded_sound)
        self.play_object = None

    def light_on_me(self):
        self.current_index += 1
        if self.current_index >= len(self.pause_sounds):
            random.shuffle(self.pause_sounds)
            self.current_index = 0

        if self.block_on_playback:
            self.play_object = play(self.pause_sounds[self.current_index])
        else:
            self.play_object = _play_with_simpleaudio(self.pause_sounds[self.current_index])

    def light_leaves_me(self):
        self.play_object.stop()
