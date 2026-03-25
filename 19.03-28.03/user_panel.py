import tkinter as tk
from tkinter import ttk, messagebox

class UserPanel:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("Панель пользователя - Молочный комбинат")
        self.window.geometry("600x400")
        
        tk.Label(self.window, text="Добро пожаловать в систему!", font=("Arial", 16)).pack(pady=50)
        tk.Label(self.window, text="Панель пользователя находится в разработке", font=("Arial", 12)).pack()
    
    def run(self):
        self.window.mainloop()