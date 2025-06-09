import tkinter as tk
from tkinter import constants as tkc
from tkinter import filedialog, messagebox, ttk
import os

# Цветовая палитра
BG_COLOR = "#1e1e1e" 
ACCENT_COLOR = "#FFA500"
TEXT_COLOR = "#ffffff"
BTN_HOVER = "#e67e00"
MENU_BG = "#2d2d2d"
PANEL_BG = "#2a2a2a"

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Текстовый редактор")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_COLOR)

        # Переменные
        self.file_path = None
        self.font_family = tk.StringVar(value="Helvetica")
        self.font_size = tk.IntVar(value=12)

        # Создание интерфейса
        self.create_widgets()
        self.create_menu()
        self.bind_shortcuts()

    def create_widgets(self):
        toolbar = tk.Frame(self.root, bg=PANEL_BG)
        toolbar.grid(row=0, sticky="ew", padx=5, pady=5)

        buttons = [
            ("📂 Открыть", self.open_file),
            ("💾 Сохранить", self.save_file),
            ("✨ Очистить", self.clear_text),
            ("📁 Новый", self.new_file),
            ("❓ Помощь", self.show_help)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(toolbar, text=text, command=command, bg=ACCENT_COLOR,
                            fg=TEXT_COLOR, activebackground=BTN_HOVER, relief=tkc.FLAT, padx=10, pady=5)
            btn.pack(side=tk.LEFT, padx=3)
            self.add_hover_effect(btn)

        font_frame = tk.Frame(toolbar, bg=PANEL_BG)
        font_frame.pack(side=tk.LEFT, padx=10)

        font_label = tk.Label(font_frame, text="Шрифт:", bg=PANEL_BG, fg=TEXT_COLOR)
        font_label.pack(side=tk.LEFT)

        font_combo = ttk.Combobox(font_frame, textvariable=self.font_family, values=[
            "Arial", "Courier", "Helvetica", "Times New Roman", "Consolas"
        ], width=15, state='readonly')
        font_combo.pack(side=tk.LEFT, padx=5)
        font_combo.bind("<<ComboboxSelected>>", lambda e: self.change_font())

        size_label = tk.Label(font_frame, text="Размер:", bg=PANEL_BG, fg=TEXT_COLOR)
        size_label.pack(side=tk.LEFT)

        size_spin = tk.Spinbox(font_frame, from_=8, to=48, textvariable=self.font_size,
                               width=5, command=self.change_font, bg=BG_COLOR, fg=TEXT_COLOR)
        size_spin.pack(side=tk.LEFT, padx=5)

        self.text_area = tk.Text(self.root, wrap="word", undo=True, font=("Helvetica", 12),
                                 bg="#111111", fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                                 selectbackground="#444444", borderwidth=2, relief="sunken")
        self.text_area.grid(row=1, sticky="nsew", padx=10, pady=5)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_menu(self):
        menu_bar = tk.Menu(self.root, bg=MENU_BG, fg=TEXT_COLOR)

        file_menu = tk.Menu(menu_bar, tearoff=0, bg=MENU_BG, fg=TEXT_COLOR)
        file_menu.add_command(label="Новый (Ctrl+N)", command=self.new_file)
        file_menu.add_command(label="Открыть (Ctrl+O)", command=self.open_file)
        file_menu.add_command(label="Сохранить (Ctrl+S)", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0, bg=MENU_BG, fg=TEXT_COLOR)
        edit_menu.add_command(label="Очистить всё", command=self.clear_text)
        edit_menu.add_command(label="Выделить всё", command=self.select_all)
        menu_bar.add_cascade(label="Правка", menu=edit_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0, bg=MENU_BG, fg=TEXT_COLOR)
        help_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Помощь", menu=help_menu)

        self.root.config(menu=menu_bar)

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-a>", lambda e: self.select_all())

    def add_hover_effect(self, widget):
        widget.bind("<Enter>", lambda e: widget.config(bg=BTN_HOVER))
        widget.bind("<Leave>", lambda e: widget.config(bg=ACCENT_COLOR))

    def new_file(self):
        if self.confirm_discard_changes():
            self.text_area.delete(1.0, tk.END)
            self.file_path = None
            self.root.title("Без имени - Текстовый редактор")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.file_path = path
            self.root.title(f"{os.path.basename(path)} - Текстовый редактор")

    def save_file(self):
        if not self.file_path:
            path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
            if not path:
                return
            self.file_path = path
            self.root.title(f"{os.path.basename(path)} - Текстовый редактор")
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(self.text_area.get(1.0, tk.END))

    def clear_text(self):
        if messagebox.askyesno("Очистка текста", "Вы уверены, что хотите очистить весь текст?"):
            self.text_area.delete(1.0, tk.END)

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", "end-1c")
        return "break"

    def change_font(self):
        family = self.font_family.get()
        size = self.font_size.get()
        self.text_area.config(font=(family, size))

    def show_help(self):
        messagebox.showinfo("Помощь", "Используйте Ctrl+O для открытия, Ctrl+S для сохранения, Ctrl+N для нового документа.")

    def show_about(self):
        messagebox.showinfo("О программе", "Текстовый редактор\nСоздан с ❤️ на Python и Tkinter.")

    def confirm_discard_changes(self):
        if self.text_area.edit_modified():
            return messagebox.askyesno("Несохранённые изменения", "У вас есть несохранённые изменения. Отменить?")
        return True


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
