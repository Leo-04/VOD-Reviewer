from tkinter import *
from tk_menu import TkMenu
from video_player import VideoPlayer
from comments import Comments
from option_dialog import OptionDialog
import os, sys
from tkinter.filedialog import *


def dir_path(p):
    return os.path.join(os.path.dirname(sys.executable), p)


class App(Tk):
    def __init__(self):
        # Set up window
        Tk.__init__(self)
        self.option_readfile(dir_path("style.txt"))
        self.minsize(800, 500)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title("VOD Reviewer")

        self.style_cnf = OptionDialog(self, "Style Config", "Select a style",
                                      ["System", "Dark", "Light", ("Cancel", None)], force_focus=False)
        self.save_option = OptionDialog(self, "Save?", "Save file?", OptionDialog.yes_no_cancel,
                                        close_on_deselect=False)
        self.restart_message = OptionDialog(self, "Restart", "The program must be restarted for this to take affect",
                                            OptionDialog.ok, close_on_deselect=False)
        self.sliding_window = PanedWindow(self, sashwidth=5, sashrelief="raised")

        # Widgets
        menu_bar = TkMenu(self)
        self.player = VideoPlayer(self.sliding_window)
        self.comments = Comments(self.sliding_window, self.player.seek_bar, width=40)

        # Menu Bar config
        menu_bar.add_command("Load", "<Control-o>", self.open)
        menu_bar.add_command("Save", "<Control-s>", self.save)
        menu_bar.add_seperator()
        menu_bar.add_command("Add Comment", "<KeyRelease-Return>", self.add_note)
        menu_bar.add_seperator()
        menu_bar.add_command("Change Style", "<Control-Alt-s>", self.change_style)
        menu_bar.add_command("Fullscreen", "<Key-F11>", self.toggle_fullscreen)

        # Window config
        self.sliding_window.add(self.player, sticky=NSEW, stretch="always", minsize=550)
        self.sliding_window.add(self.comments, sticky=NSEW, stretch="never")

        # Grid config
        menu_bar.grid(row=0, column=1, sticky=EW)
        self.sliding_window.grid(row=1, column=1, sticky=NSEW)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        self.file = None

    def open(self):
        filename = askopenfilename(
            title="Load VOD video",
            filetypes=(
                ("Video Files", "*.mp4"),
                ("Data Files", "*.json"),
                ("Any File", "*.*"),
            )
        )

        if filename:
            path = os.path.dirname(filename)
            title = os.path.splitext(os.path.basename(filename))[0]
            data_filename = os.path.join(path, title + ".txt")
            video_filename = os.path.join(path, title + ".mp4")
            self.player.set_file(title, video_filename)
            if os.path.exists(data_filename):
                with open(data_filename) as fp:
                    self.comments.set_text(fp.read())
            else:
                with open(data_filename, "w") as fp:
                    fp.write("")

            self.file = data_filename
            self.title("VOD Reviewer: " + title)

    def save(self):
        if self.file:
            with open(self.file, "w") as fp:
                fp.write(self.comments.get_text())

    def add_note(self):
        time = self.player.get_time()
        self.comments.insert("end", "\n\n@" + time + ":\n\t")
        self.comments.on_edit()
        self.comments.focus()
        self.player.control_bar.pause()

    def change_style(self):
        result = self.style_cnf.get_result()

        if result == "System":
            with open(dir_path("style.txt"), "w") as fp:
                fp.write("")
        elif result == "Light":
            with open(dir_path("style.txt"), "w") as fp1:
                with open(dir_path("light.txt"), "r") as fp2:
                    fp1.write(fp2.read())
        elif result == "Dark":
            with open(dir_path("style.txt"), "w") as fp1:
                with open(dir_path("dark.txt"), "r") as fp2:
                    fp1.write(fp2.read())
        else:
            return

        self.restart_message.get_result()

    def close(self):
        if self.file:
            ans = self.save_option.get_result()
        else:
            ans = False

        if ans:
            self.save()
        elif ans is not None:
            self.player.close()
            self.destroy()

    def toggle_fullscreen(self):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))
