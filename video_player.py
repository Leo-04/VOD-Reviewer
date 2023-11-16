from tkinter import *
from menu_button import MenuButton
from seeker import Seeker
from player import Player
from resize_label import ResizeLabel
from player_controls import PlayerControls


class VideoPlayer(Frame):
    def __init__(self, parent, font=(None, 20, "bold")):
        Frame.__init__(self, parent)

        # Get current style fg and bg
        temp = Label(self)
        fg = temp["fg"]
        temp.destroy()
        bg = self["bg"]

        # Widget config
        self.player = Player(self)
        self.title = ResizeLabel(self, text="", fg=fg, bg=bg)
        self.control_bar = PlayerControls(self, player=self.player)
        self.seek_bar = Seeker(self, player=self.player, height=25, fg=fg, bg=bg)
        option_pannel = Frame(self, width=0)

        # Option pannel config
        option_pannel.pack_propagate(False)

        self.vol_slider = Scale(self, orient=VERTICAL, from_=200, to=0, length=200, command=self.update_vol)
        self.vol_slider.set(100)
        self.vol = MenuButton(option_pannel, text="🔊", font=font, relx=0, rely=-4.4, widget=self.vol_slider)  # 🔇🔈🔉🔊
        self.vol.pack(side=RIGHT)

        self.speed = Spinbox(option_pannel, values=["0.25x", "0.5x", "1x", "2x", "5x", "10x"],
                             command=self.update_speed, font=font, width=5)
        self.speed.delete(0, 10)
        self.speed.insert(0, "1x")
        self.speed.config(state="readonly")
        self.speed.pack(side=RIGHT, padx=10)

        # Grid config
        self.player.grid(row=1, column=1, columnspan=3, sticky=NSEW)
        self.seek_bar.grid(row=2, column=1, columnspan=3, sticky=EW)
        self.title.grid(row=3, column=1, sticky=NSEW, pady=25, padx=(10, 0))
        self.control_bar.grid(row=3, column=2, pady=25)
        option_pannel.grid(row=3, column=3, sticky=NSEW, pady=25, padx=(0, 10))

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)

    def update_loop(self):
        self.seek_bar.update_text()
        self.seek_bar.after(1, self.update_loop)

    def update_vol(self, _):
        val = self.vol_slider.get() / 100
        self.player.set_vol(val)

        if val >= 1:
            self.vol["text"] = "🔊"
        elif val >= 0.5:
            self.vol["text"] = "🔉"
        elif val > 0:
            self.vol["text"] = "🔈"
        else:
            self.vol["text"] = "🔇"

    def update_speed(self, _=None):
        self.player.set_speed(float(self.speed.get()[:-1]))

    def close(self):
        self.player.close()

    def get_time(self):
        return Seeker.format_ms(self.player.get_pos())

    def load_file(self, filename):
        self.player.set_file(filename)

    def pause(self):
        self.seek_bar.pause()

    def set_file(self, title, filename):
        self.title.set_text(title)
        self.player.set_file(filename)
        self.player.play()
        self.player.set_pos(0)
