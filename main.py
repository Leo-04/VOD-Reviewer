# https://www.scrollseek.com/wd/html_symbols_complete.html
from tkinter import PhotoImage
from app import App, dir_path, os

light_style = '!Defaults\n    *Foreground: #333333\n\n    *Background: #CCCCCC\n    *troughColor: #CCCCCC\n\n    *activeBackground: #999999\n\n    *activeForeground: #333333\n\n    *disabledForeground: #989898\n\n    *HighlightBackground: #00FFFF\n    *HighlightColor: #00FFFF\n\n    *selectForeground: #333333\n    *selectBackground: #00FFFF\n    *selectColor: #00FFFF\n\n    *insertBackground: #333333\n\n!Buttons\n    !overRelief\n    *Spinbox.buttonBackground: #DDDDDD\n    *Spinbox.disabledBackground: #555555\n    *Spinbox.readonlyBackground: #DDDDDD\n\n!Frames\n    *Frame.HighlightColor: #00FFFF\n    *Frame.HighlightBackground: #00FFFF\n\n!Menus\n    !activeBorderWidth\n    *Menu.activeBackground: #00FFFF\n    *Menu.activeForeground: #FFFFFF\n    *Menu.font: TkDefaultFont 8\n    *Menubutton.HighlightBackground: #DDDDDD\n    *Menubutton.HighlightColor: #DDDDDD\n\n!Text\n    *Text.inactiveSelectBackground: #00FFFF\n    *Text.Background: #EEEEEE\n    *Entry.Background: #EEEEEE\n\n!Listbox\n    !Can be dotbox\n    *Listbox.activeStyle: underline\n    !*Listbox.selectBorderWidth: 2\n'
dark_style = '!Defaults\n    *foreground: #DDDDDD\n    *insertBackground: #DDDDDD\n\n    *background: #222222\n    *troughColor: #222222\n\n    *activeBackground: #999999\n\n    *activeForeground: #333333\n\n    *disabledForeground: #989898\n    *disabledBackground: #555555\n\n    *HighlightBackground: #0000FF\n    *HighlightColor: #0000FF\n\n    *selectForeground: #FFFFFF\n    *selectBackground: #0000FF\n    *selectColor: #0000FF\n\n!Buttons\n    !overRelief\n    *Spinbox.buttonBackground: #222222\n    *Spinbox.disabledBackground: #555555\n    *Spinbox.readonlyBackground: #222222\n\n!Frames\n    *Frame.HighlightColor: #0000FF\n    *Frame.HighlightBackground: #0000FF\n\n!Menus\n    !Menu.activeBorderWidth: 2\n    *Menu.activeBackground: #0000FF\n    *Menu.activeForeground: #FFFFFF\n    *Menu.font: TkDefaultFont 8\n    *Menubutton.HighlightBackground: #222222\n    *Menubutton.HighlightColor: #222222\n\n!Textbox\n    *Text.inactiveSelectBackground: #0000FF\n    *Text.Background: #333333\n    *Entry.Background: #333333\n\n!Listbox\n    !Can be dotbox\n    *Listbox.activeStyle: underline\n    !*Listbox.selectBorderWidth: 2\n'

icon_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x04\x03\x00\x00\x00\xed\xdd\xe2R\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tPLTE\x00\x00\x00\xff\xff\xff\x00\xff\xff\xcd\xe0\x91\x8e\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00;IDAT\x18\xd3c\x80\x03F\x01A0B\x88\x082\n\x02\x81\x80 \x88\xc1\x00e\x08(1B\x18LJ\nh\x0c\xb8\x94 \x83\x00#\x84!(\xc0\x00e\x08\xc2\x19 5\xb8,e`\x00\x00s\x9b\x05\x1d\x99\x9b1\x88\x00\x00\x00\x00IEND\xaeB`\x82'


def main():
    if not os.path.exists(dir_path("light.txt")):
        with open("light.txt", "w") as fp:
            fp.write(light_style)

    if not os.path.exists(dir_path("dark.txt")):
        with open("dark.txt", "w") as fp:
            fp.write(dark_style)

    if not os.path.exists(dir_path("style.txt")):
        with open("style.txt", "w") as fp:
            fp.write(dark_style)

    app = App()
    app.iconphoto(False, PhotoImage(data=icon_data))
    app.player.update_loop()
    app.mainloop()


if __name__ == "__main__":
    main()

# ⁽⁽╳⚑⛿✎
