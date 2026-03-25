import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os

class CaptchaDialog:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Проверка CAPTCHA")
        self.window.geometry("450x500")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.correct_order = [1, 2, 3, 4]
        self.shuffled_order = []
        self.selected_order = []
        self.buttons = []
        self.images = []
        
        self.setup_ui()
        self.generate_captcha()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Нажмите на картинки в правильном порядке", 
                font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(main_frame, text="Правильный порядок: 1 → 2 → 3 → 4", 
                font=("Arial", 10), fg="blue").pack(pady=5)
        
        self.info_label = tk.Label(main_frame, text="Выбрано: 0/4", 
                                   font=("Arial", 10), fg="green")
        self.info_label.pack(pady=5)
        
        self.grid_frame = tk.Frame(main_frame)
        self.grid_frame.pack(pady=10)
        
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Сбросить", command=self.reset_captcha, 
                 width=15, height=1, bg="orange").pack(side=tk.LEFT, padx=5)
        
    def generate_captcha(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        self.shuffled_order = random.sample(self.correct_order, 4)
        self.buttons = []
        self.images = []
        self.selected_order = []
        self.info_label.config(text="Выбрано: 0/4")
        
        positions = [(0,0), (0,1), (1,0), (1,1)]
        
        for i, pos in enumerate(positions):
            number = self.shuffled_order[i]
            img = self.load_image(f"images/piece{number}.png")
            self.images.append(img)
            
            btn = tk.Button(self.grid_frame, image=img, width=150, height=150,
                          command=lambda n=number, idx=i: self.on_button_click(n, idx))
            btn.grid(row=pos[0], column=pos[1], padx=5, pady=5)
            btn.config(bg="white", relief=tk.RAISED)
            self.buttons.append({"button": btn, "number": number, "clicked": False, "idx": i})
    
    def load_image(self, path):
        try:
            if os.path.exists(path):
                img = Image.open(path)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            else:
                img = Image.new('RGB', (150, 150), color='lightgray')
                return ImageTk.PhotoImage(img)
        except:
            img = Image.new('RGB', (150, 150), color='lightgray')
            return ImageTk.PhotoImage(img)
    
    def on_button_click(self, number, idx):
        for btn in self.buttons:
            if btn["number"] == number and btn["clicked"]:
                messagebox.showwarning("Ошибка", f"Картинка {number} уже выбрана")
                return
        
        expected = len(self.selected_order) + 1
        
        if number == expected:
            self.selected_order.append(number)
            for btn in self.buttons:
                if btn["number"] == number:
                    btn["clicked"] = True
                    btn["button"].config(bg="lightgreen", relief=tk.SUNKEN)
                    break
            self.info_label.config(text=f"Выбрано: {len(self.selected_order)}/4")
            
            if len(self.selected_order) == 4:
                self.check_captcha()
        else:
            messagebox.showwarning("Ошибка", f"Нужно выбрать картинку {expected}")
    
    def reset_captcha(self):
        self.generate_captcha()
    
    def check_captcha(self):
        if self.selected_order == self.correct_order:
            self.result = True
            self.window.destroy()
        else:
            messagebox.showerror("Ошибка", "Неправильный порядок. Попробуйте еще раз.")
            self.generate_captcha()
    
    def show(self):
        self.window.wait_window()
        return getattr(self, 'result', False)