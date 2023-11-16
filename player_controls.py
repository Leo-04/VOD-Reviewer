from tkinter import Frame, Button


class PlayerControls(Frame):
    PAUSE = "⏐⏐"  # ⏸
    PLAY = "▶"
    REPLAY = "⟳"
    SKIP_LEFT = "ᐸᐸ"
    SKIP_RIGHT = "ᐳᐳ"

    SKIP_AMOUNT = 5

    def __init__(self, master=None, cnf=None, **kwargs):
        if cnf is None:
            cnf = {}

        cnf.update(kwargs)

        font = (None, 20, "bold")
        if "font" in cnf:
            font = cnf.pop("font")

        self.player = None
        if "player" in cnf:
            self.player = cnf.pop("player")
            self.player.on_end(self.on_end)

        Frame.__init__(self, master, cnf)

        self.skip_back = Button(self, text=str(PlayerControls.SKIP_AMOUNT) + PlayerControls.SKIP_LEFT, font=font,
                                command=lambda: self.skip(-PlayerControls.SKIP_AMOUNT))
        self.play_button = Button(self, text=PlayerControls.PAUSE, font=font, command=self.play_pause, width=3)
        self.skip_forward = Button(self, text=PlayerControls.SKIP_RIGHT + str(PlayerControls.SKIP_AMOUNT), font=font,
                                   command=lambda: self.skip(PlayerControls.SKIP_AMOUNT))

        self.skip_back.grid(row=0, column=1)
        self.play_button.grid(row=0, column=2)
        self.skip_forward.grid(row=0, column=3)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(4, weight=1)

        self.winfo_toplevel().bind("<KeyRelease-space>", lambda e: self.play_pause())
        self.winfo_toplevel().bind("<KeyRelease-Left>", lambda e: self.skip(-PlayerControls.SKIP_AMOUNT))
        self.winfo_toplevel().bind("<KeyRelease-Right>", lambda e: self.skip(PlayerControls.SKIP_AMOUNT))

    def on_end(self):
        self.play_button["text"] = PlayerControls.REPLAY

    def restart(self):
        self.player.play()
        self.player.goto(0)
        self.play_button["text"] = PlayerControls.PAUSE

    def play(self):
        self.player.unpause()
        self.play_button["text"] = PlayerControls.PAUSE

    def pause(self):
        self.player.pause()
        self.play_button["text"] = PlayerControls.PLAY

    def play_pause(self):
        if self.player is not None:
            if self.player.has_ended():
                self.restart()
            elif self.player.is_paused():
                self.play()
            else:
                self.pause()

    def skip(self, i):
        if self.player is not None:
            self.player.skip(i)
