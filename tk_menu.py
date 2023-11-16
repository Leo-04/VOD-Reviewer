from tkinter import Frame, Label, Button


class TkMenu(Frame):
    def __init__(self, master, *commands):
        Frame.__init__(self, master, bd=2, relief="raised")

        for cmd in commands:
            if cmd is None:
                self.add_seperator()
            else:
                self.add_command(*cmd)

    def add_seperator(self, size=20, side="left"):
        """Adds a seperator"""

        Label(self, padx=size).pack(side=side)

    def add_command(self, name, hotkey=None, callback=lambda: None, side="left"):
        """Adds a button to the menu"""

        button = Button(self, text=name, command=callback, padx=10, pady=2, relief="flat")
        button.pack(side=side)
        button.bind("<ButtonPress-1>", lambda e: button.config(relief="sunken"))
        button.bind("<ButtonRelease-1>", lambda e: button.config(relief="flat"))

        self.winfo_toplevel().bind_all(hotkey, lambda e: callback())
