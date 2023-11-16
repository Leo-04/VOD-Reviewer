from tkinter import Button


class MenuButton(Button):
    def __init__(self, master=None, cnf=None, relx=0, rely=0, **kwargs):
        if cnf is None:
            cnf = {}

        cnf.update(kwargs)

        self.shown = False
        self.widget = None
        if "widget" in cnf:
            self.widget = cnf.pop("widget")

        self.relx = relx
        self.rely = rely

        Button.__init__(self, master, cnf, relief="flat")
        self.bind("<ButtonPress-1>", lambda e: self.config(relief="sunken"))
        self.bind("<ButtonRelease-1>", lambda e: (self.config(relief="flat"), self.toggle()))

        self.set_widget(self.widget)

    def toggle(self):
        if self.shown:
            self.shown = False
            self.widget.place_forget()
        else:
            self.shown = True

            self.widget.place(
                relx=self.relx,
                rely=self.rely,
                in_=self,
            )
            self.widget.focus()

    def set_widget(self, widget):
        self.widget = widget
        self.shown = False
