import tkinter as tk
from tkinter import messagebox
from database import Database
from captcha import CaptchaDialog

class LoginForm:
    def __init__(self):
        self.db = Database()
        self.window = tk.Tk()
        self.window.title("Авторизация - Молочный комбинат")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        self.current_username = None
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Авторизация в системе", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(main_frame, text="Логин:", font=("Arial", 10)).pack(anchor=tk.W)
        self.entry_login = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.entry_login.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(main_frame, text="Пароль:", font=("Arial", 10)).pack(anchor=tk.W)
        self.entry_password = tk.Entry(main_frame, font=("Arial", 10), width=30, show="*")
        self.entry_password.pack(fill=tk.X, pady=(0, 20))
        
        self.btn_login = tk.Button(main_frame, text="Войти", font=("Arial", 10), command=self.login, width=20)
        self.btn_login.pack(pady=10)
        
        self.entry_login.bind("<Return>", lambda e: self.entry_password.focus())
        self.entry_password.bind("<Return>", lambda e: self.login())
    
    def login(self):
        username = self.entry_login.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Предупреждение", "Логин и пароль обязательны для заполнения")
            return
        
        self.current_username = username
        
        result = self.db.validate_user(username, password)
        
        if result is None:
            messagebox.showerror("Ошибка", "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные")
            self.db.update_failed_attempts(username, True)
            self.check_and_block(username)
            return
        
        role, is_blocked, failed_attempts = result
        
        if is_blocked:
            messagebox.showerror("Ошибка", "Вы заблокированы. Обратитесь к администратору")
            return
        
        captcha = CaptchaDialog(self.window)
        if not captcha.show():
            self.db.update_failed_attempts(username, True)
            self.check_and_block(username)
            messagebox.showerror("Ошибка", "Пазл собран неверно. Попробуйте еще раз.")
            return
        
        self.db.update_failed_attempts(username, False)
        messagebox.showinfo("Успех", "Вы успешно авторизовались")
        
        self.window.destroy()
        
        if role == "Администратор":
            from admin_panel import AdminPanel
            admin = AdminPanel(self.db)
            admin.run()
        else:
            from user_panel import UserPanel
            user = UserPanel(self.db)
            user.run()
    
    def check_and_block(self, username):
        result = self.db.validate_user(username, "")
        if result:
            _, _, failed_attempts = result
            if failed_attempts >= 3:
                self.db.block_user(username)
                messagebox.showerror("Ошибка", "Вы заблокированы. Обратитесь к администратору")
    
    def run(self):
        self.window.mainloop()