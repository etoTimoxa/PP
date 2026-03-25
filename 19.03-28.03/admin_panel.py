import tkinter as tk
from tkinter import ttk, messagebox

class AdminPanel:
    def __init__(self, db):
        self.db = db
        self.window = tk.Tk()
        self.window.title("Панель администратора - Молочный комбинат")
        self.window.geometry("800x500")
        
        self.setup_ui()
        self.load_users()
    
    def setup_ui(self):
        toolbar = tk.Frame(self.window, bg="#f0f0f0", height=40)
        toolbar.pack(fill=tk.X)
        
        tk.Button(toolbar, text="Добавить пользователя", command=self.add_user).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Редактировать", command=self.edit_user).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Удалить", command=self.delete_user).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text="Снять блокировку", command=self.unblock_user).pack(side=tk.LEFT, padx=5, pady=5)
        
        main_frame = tk.Frame(self.window, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "username", "role", "is_blocked", "failed_attempts")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Логин")
        self.tree.heading("role", text="Роль")
        self.tree.heading("is_blocked", text="Заблокирован")
        self.tree.heading("failed_attempts", text="Ошибок")
        
        self.tree.column("id", width=50)
        self.tree.column("username", width=150)
        self.tree.column("role", width=120)
        self.tree.column("is_blocked", width=100)
        self.tree.column("failed_attempts", width=80)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        users = self.db.get_all_users()
        for user in users:
            self.tree.insert("", tk.END, values=(
                user[0], user[1], user[2], "Да" if user[3] else "Нет", user[4]
            ))
    
    def add_user(self):
        dialog = tk.Toplevel(self.window)
        dialog.title("Добавление пользователя")
        dialog.geometry("300x250")
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Логин:").pack(pady=(20, 5))
        entry_login = tk.Entry(dialog)
        entry_login.pack()
        
        tk.Label(dialog, text="Пароль:").pack(pady=(10, 5))
        entry_password = tk.Entry(dialog, show="*")
        entry_password.pack()
        
        tk.Label(dialog, text="Роль:").pack(pady=(10, 5))
        combo_role = ttk.Combobox(dialog, values=["Пользователь", "Администратор"])
        combo_role.current(0)
        combo_role.pack()
        
        def save():
            login = entry_login.get().strip()
            password = entry_password.get().strip()
            role = combo_role.get()
            
            if not login or not password:
                messagebox.showwarning("Ошибка", "Логин и пароль обязательны")
                return
            
            if self.db.user_exists(login):
                messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
                return
            
            self.db.add_user(login, password, role)
            messagebox.showinfo("Успех", "Пользователь добавлен")
            dialog.destroy()
            self.load_users()
        
        tk.Button(dialog, text="Сохранить", command=save).pack(pady=20)
    
    def edit_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите пользователя")
            return
        
        values = self.tree.item(selected[0])["values"]
        user_id, username, role, is_blocked, failed_attempts = values
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Редактирование пользователя")
        dialog.geometry("300x320")
        dialog.transient(self.window)
        dialog.grab_set()
        
        tk.Label(dialog, text="Логин:").pack(pady=(20, 5))
        entry_login = tk.Entry(dialog)
        entry_login.insert(0, username)
        entry_login.pack()
        
        tk.Label(dialog, text="Новый пароль (оставьте пустым, чтобы не менять):").pack(pady=(10, 5))
        entry_password = tk.Entry(dialog, show="*")
        entry_password.pack()
        
        tk.Label(dialog, text="Роль:").pack(pady=(10, 5))
        combo_role = ttk.Combobox(dialog, values=["Пользователь", "Администратор"])
        combo_role.set(role)
        combo_role.pack()
        
        blocked_var = tk.BooleanVar(value=(is_blocked == "Да"))
        tk.Checkbutton(dialog, text="Заблокирован", variable=blocked_var).pack(pady=10)
        
        def save():
            new_login = entry_login.get().strip()
            new_password = entry_password.get().strip()
            new_role = combo_role.get()
            new_blocked = blocked_var.get()
            
            if not new_login:
                messagebox.showwarning("Ошибка", "Логин обязателен")
                return
            
            if not new_password:
                new_password = None
            
            self.db.update_user(user_id, new_login, new_password, new_role, new_blocked)
            messagebox.showinfo("Успех", "Данные обновлены")
            dialog.destroy()
            self.load_users()
        
        tk.Button(dialog, text="Сохранить", command=save).pack(pady=20)
    
    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите пользователя")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить пользователя?"):
            user_id = self.tree.item(selected[0])["values"][0]
            self.db.delete_user(user_id)
            self.load_users()
    
    def unblock_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите пользователя")
            return
        
        user_id = self.tree.item(selected[0])["values"][0]
        
        try:
            self.db.unblock_user(user_id)
            self.load_users()
            messagebox.showinfo("Успех", "Блокировка снята")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось снять блокировку: {e}")
    
    def run(self):
        self.window.mainloop()