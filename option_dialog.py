from tkinter import *


class OptionDialog(Toplevel):
    yes_no_cancel = (("Yes", True), ("No", False), ("Cancel", None))
    yes_no = (("Yes", True), ("No", False))
    ok_cancel = (("Ok", True), ("Cancel", None))
    retry_cancel = (("Retry", True), ("Cancel", None))
    ok = (("Ok", True),)

    def __init__(self, root, title, message, options=ok, width=300, height=200, default=None, close_on_deselect=True,
                 force_focus=True):
        Toplevel.__init__(self, root)
        self.withdraw()
        self.overrideredirect(True)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.config(relief="ridge", bd=1)

        self.geometry("%sx%s" % (
            width, height
        ))

        self.title_label = Label(self, text=title, relief="ridge", bd=3)
        self.close = Button(self.title_label, text="╳", bg="red", relief="flat", command=self.on_close)
        self.message = Message(self, text=message, width=width)
        self.buttons = Frame(self, relief="raised", bd=1)

        for option in options:
            if type(option) in [tuple, list]:
                item = option[0]
                value = option[1]
            else:
                item = option
                value = option

            Button(self.buttons, text=item, command=lambda val=value: self.set_option(val)).pack(side=LEFT, fill=X,
                                                                                                 padx=10, pady=10,
                                                                                                 expand=1)

        self.title_label.pack(side=TOP, fill=X)
        self.message.pack(side=TOP, fill=BOTH, expand=1)
        self.buttons.pack(side=BOTTOM, fill=X)
        self.close.pack(side=RIGHT)

        if close_on_deselect:
            self.bind("<FocusOut>", lambda e: self.on_close())

        self.title_label.bind("<ButtonPress-1>", self.press_title)
        self.title_label.bind("<B1-Motion>", self.drag_title)

        self.option = Variable(self, value=None)
        self.root = root
        self.width = width
        self.height = height
        self.default = default
        self.dx = 0
        self.dy = 0
        self.close_on_deselect = close_on_deselect
        self.force_focus = force_focus

    def press_title(self, event):
        self.dx = event.x_root - self.winfo_x()
        self.dy = event.y_root - self.winfo_y()

    def drag_title(self, event):

        self.geometry("+%s+%s" % (
            event.x_root - self.dx,
            event.y_root - self.dy
        ))

    def set_option(self, option):
        self.option.set(option)

    def on_close(self):
        self.set_option(self.default)

    def get_result(self):
        self.option.set(self.default)

        self.geometry("+%s+%s" % (
            self.root.winfo_x() + (self.root.winfo_width() - self.width) // 2,
            self.root.winfo_y() + (self.root.winfo_height() - self.height) // 2,
        ))

        self.deiconify()
        self.update()
        self.focus()
        if self.force_focus:
            self.grab_set()
        self.wait_variable(self.option)
        if self.force_focus:
            self.grab_release()
        self.withdraw()

        return self.option.get()
