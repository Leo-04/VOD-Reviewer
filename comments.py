from tkinter import Text
import re


class Comments(Text):
    regex = re.compile(r"^\s*\@\d+:\d+:\d+", re.MULTILINE)

    def __init__(self, parent, seeker, **kwargs):
        Text.__init__(self, parent, **kwargs)

        self.seeker = seeker
        self.items = {}

        self.bind("<Configure>", self.on_resize)
        self.bind("<KeyRelease>", self.on_edit)
        self.bind("<Escape>", lambda e: self.master.focus())

    def set_text(self, text):
        self.delete("1.0", "end")
        self.insert("end", text)
        self.on_edit()

    def get_text(self):
        return self.get("1.0", "end-1c")

    def on_resize(self, e=None):
        for item in self.items:
            self.seeker.coords(item, self.seeker.get_x(self.items[item]), 0)

    def on_edit(self, *events):
        times = Comments.regex.findall(self.get("1.0", "end"))

        new_times = []
        for time in times:
            h, m, s = time.strip()[1:].split(":")
            time_stamp = ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000
            new_times.append(time_stamp)

        if set(new_times) != set(self.items.values()):
            for item in self.items:
                self.seeker.delete(item)

            for time in new_times:
                item = self.seeker.create_text(self.seeker.get_x(time), 0, text="⚑", anchor="n", fill="red")
                self.items[item] = time
                self.seeker.bind("<Button-3>", lambda e: self.seeker.player.set_pos(time))

        self.on_resize()

        return "break"
