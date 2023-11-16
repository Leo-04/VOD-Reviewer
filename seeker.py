from tkinter import Canvas
from tkinter.font import Font


class Seeker(Canvas):
    def __init__(self, master=None, cnf=None, **kwargs):
        if cnf is None:
            cnf = {}

        cnf.update(kwargs)

        self.font = Font(font=(None, 10, "bold"))
        if "font" in cnf:
            self.font = cnf.pop("font")

        self.player = None
        if "player" in cnf:
            self.player = cnf.pop("player")

        self.line_padding = 10
        if "line_padding" in cnf:
            self.line_padding = cnf.pop("line_padding")

        self.fg = "black"
        if "fg" in cnf:
            self.fg = cnf.pop("fg")

        if "bg" not in cnf:
            cnf["bg"] = "white"

        self.line_width = 2
        self.seek_size = 10

        Canvas.__init__(self, master, cnf, bd=0, highlightthickness=0)

        while self.font.metrics()['linespace'] <= int(self["height"]):
            self.font.config(size=self.font.cget("size") + 1)
        # self.font.config(size=self.font.cget("size") - 1)

        self.update()
        self.start = self.create_text(0, 0, anchor="nw", text=" " + Seeker.format_ms(0), font=self.font, fill=self.fg)
        self.end = self.create_text(self.winfo_width(), 0, anchor="ne", text=Seeker.format_ms(0) + " ", font=self.font,
                                    fill=self.fg)

        self.line = self.create_rectangle(0, 0, 0, 0, fill=self.fg, outline="")
        self.seek = self.create_oval(0, 0, 0, 0, fill=self.fg, outline=self["bg"])
        self.resized = True

        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.line_pressed)
        self.bind("<B1-Motion>", self.line_pressed)
        self.tag_bind(self.seek, "<B1-Motion>", self.line_pressed)

    @staticmethod
    def format_ms(ms):
        h = ms // (1000 * 60 * 60)
        m = (ms // (1000 * 60)) % 60
        s = (ms // 1000) % 60
        ms = ms % 1000
        return "%02d:%02d:%02d" % (h, m, s)  # .%04d ms

    def on_resize(self, event=None):
        self.resized = True

    def get_pos(self, x, y):
        if self.player is None:
            return

        pos = self.player.get_pos()
        if pos == -1:
            return
        end = self.player.get_end()
        if end == -1:
            return

        current = " " + Seeker.format_ms(pos)
        ending = Seeker.format_ms(end) + " "
        width_pos = self.font.measure(current)
        width_end = self.font.measure(ending)
        p = ((x - (width_pos + self.line_padding)) / (
                    self.winfo_width() - width_end - 2 * self.line_padding - width_pos))
        if p < 0 or p > 1:
            return None

        new_pos = p * end

        return new_pos

    def get_x(self, pos):
        if self.player is None:
            return

        end = self.player.get_end()
        if end == 0:
            return 0

        current = " " + Seeker.format_ms(pos)
        ending = Seeker.format_ms(end) + " "
        width_pos = self.font.measure(current)
        width_end = self.font.measure(ending)
        p = pos / end

        if p < 0:
            p = 0
        if p > 1:
            p = 1

        x = (p * (self.winfo_width() - width_end - 2 * self.line_padding - width_pos)) + (width_pos + self.line_padding)

        return x

    def line_pressed(self, event):
        new_pos = self.get_pos(event.x, event.y)

        if new_pos is not None:
            self.player.set_pos(int(new_pos))

    def update_text(self):
        pos = 0
        end = 0
        if self.player:
            pos = self.player.get_pos()
            if pos == -1:
                pos = 0
            end = self.player.get_end()
            if end == -1:
                end = 0

        current = " " + Seeker.format_ms(pos)
        ending = Seeker.format_ms(end) + " "

        self.itemconfig(self.start, text=current)
        self.itemconfig(self.end, text=ending)

        width_pos = self.font.measure(current)
        width_end = self.font.measure(ending)

        if end > 0:
            percentage = pos / end
            current_pos = percentage * (self.winfo_width() - (width_end + width_pos) - 2 * self.line_padding)
            self.coords(
                self.seek,
                current_pos + width_pos - self.seek_size / 2 + self.line_padding,
                (self.winfo_height() - self.seek_size) / 2,
                current_pos + width_pos + self.seek_size / 2 + self.line_padding,
                (self.winfo_height() + self.seek_size) / 2,
            )
        else:
            self.coords(
                self.seek,
                -100, 0, 0, 0
            )

        if self.resized:
            self.coords(self.end, self.winfo_width(), 0)
            self.coords(
                self.line,
                width_pos + self.line_padding,
                self.winfo_height() / 2 - self.line_width / 2,
                self.winfo_width() - width_end - self.line_padding,
                self.winfo_height() / 2 + self.line_width / 2
            )
            self.resized = False
