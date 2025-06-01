import sys
import tkinter.filedialog
from tkinter import *

root = Tk()
root.title("Text Editor")

text = Text(root)
text.grid()

# Меню шрифтов через радиокнопки
selected_font = StringVar(value="Helvetica")

def change_font():
    font_name = selected_font.get()
    text.config(font=font_name)

font_button = Menubutton(root, text="Font")
font_button.grid()

font_menu = Menu(font_button, tearoff=0)
font_button["menu"] = font_menu

font_menu.add_radiobutton(label="Helvetica", variable=selected_font, value="Helvetica", command=change_font)
font_menu.add_radiobutton(label="Courier", variable=selected_font, value="Courier", command=change_font)

root.mainloop()
