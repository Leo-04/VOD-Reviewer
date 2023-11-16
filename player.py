from tkinter import Canvas
import vlc

import os
os.add_dll_directory(os.getcwd())
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')


class Player(Canvas):
    def __init__(self, parent, *args, **kwargs):
        Canvas.__init__(self, parent, bg='black')

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(self.winfo_id())

    def set_file(self, _source):
        Media = self.instance.media_new(_source)
        Media.get_mrl()
        self.player.set_media(Media)

    def has_ended(self):
        return self.player.get_state() == vlc.State.Ended

    def play(self):
        if self.player.get_state() == vlc.State.Ended:
            self.player.set_media(self.player.get_media())

        self.player.play()

    def close(self):
        self.player.stop()

    def pause(self):
        self.player.set_pause(True)

    def unpause(self):
        self.player.set_pause(False)

    def is_paused(self):
        return not self.player.is_playing()

    def skip(self, s):
        self.set_pos(self.player.get_time() + s * 1000)

    def get_end(self):
        return self.player.get_length()

    def get_pos(self):
        return self.player.get_time()

    def set_pos(self, t):
        if t < 0:
            t = 0

        self.player.set_time(t)

    def goto(self, p):
        self.player.set_position(p)

    def set_vol(self, p):
        self.player.audio_set_volume(int(100 * p))

    def set_speed(self, speed):
        self.player.set_rate(speed)

    def on_end(self, callback):
        self.player.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, lambda event: callback())
