from tkinter import Canvas
from tkinter.font import Font


class ResizeLabel(Canvas):
    def __init__(self, master=None, cnf=None, **kwargs):
        if cnf is None:
            cnf = {}

        cnf.update(kwargs)

        self.font = Font(font=(None, 10, "bold"))
        if "font" in cnf:
            self.font = cnf.pop("font")

        self.fg = "black"
        if "fg" in cnf:
            self.fg = cnf.pop("fg")

        if "bg" not in cnf:
            cnf["bg"] = "white"

        self.text = ""
        if "text" in cnf:
            self.text = cnf.pop("text")

        self.line_width = 2
        self.seek_size = 10

        Canvas.__init__(self, master, cnf, bd=0, highlightthickness=0, width=0, height=0)
        self.text_tag = self.create_text(0, 0, anchor="w", text=self.text, fill=self.fg)

        self.bind("<Configure>", self.on_resize)

        self.set_text(self.text)

    def set_text(self, text=""):
        text = " " + text + " "
        self.itemconfig(self.text_tag, text=text)
        self.text = text
        self.on_resize()

    def on_resize(self, event=None):
        self.font.config(size=1)
        while self.font.metrics()['linespace'] <= self.winfo_height():
            self.font.config(size=self.font.cget("size") + 1)
        self.font.config(size=self.font.cget("size") // 2 + 1)

        self.itemconfig(self.text_tag, font=self.font)
        self.coords(self.text_tag, 0, self.winfo_height() / 2)

        if self.font.measure(self.text) > self.winfo_width():
            text = self.text
            while self.font.measure(text + "... ") > self.winfo_width() and text.strip() != "":
                text = text[:-1]

            self.itemconfig(self.text_tag, text=text + "... ")
        else:
            self.itemconfig(self.text_tag, text=self.text)
