import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                port="5432",
                database="proizvodstvo",
                user="postgres",
                password="postgres"
            )
            self.conn.autocommit = False
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            raise
    
    def validate_user(self, username, password):
        try:
            if password:
                query = "SELECT role, is_blocked, failed_attempts FROM users WHERE username = %s AND password_hash = %s"
                self.cursor.execute(query, (username, password))
            else:
                query = "SELECT role, is_blocked, failed_attempts FROM users WHERE username = %s"
                self.cursor.execute(query, (username,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.conn.rollback()
            return None
    
    def update_failed_attempts(self, username, increment=True):
        try:
            if increment:
                query = "UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = %s"
                self.cursor.execute(query, (username,))
            else:
                query = "UPDATE users SET failed_attempts = 0 WHERE username = %s"
                self.cursor.execute(query, (username,))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка обновления попыток: {e}")
            self.conn.rollback()
    
    def block_user(self, username):
        try:
            query = "UPDATE users SET is_blocked = true WHERE username = %s"
            self.cursor.execute(query, (username,))
            self.conn.commit()
            print(f"Пользователь {username} заблокирован")
        except Exception as e:
            print(f"Ошибка блокировки: {e}")
            self.conn.rollback()
    
    def unblock_user(self, user_id):
        try:
            query = "UPDATE users SET is_blocked = false, failed_attempts = 0 WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка снятия блокировки: {e}")
            self.conn.rollback()
    
    def get_all_users(self):
        try:
            query = "SELECT id, username, role, is_blocked, failed_attempts FROM users ORDER BY id"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения пользователей: {e}")
            self.conn.rollback()
            return []
    
    def add_user(self, username, password, role):
        try:
            query = "INSERT INTO users (username, password_hash, role, is_blocked, failed_attempts) VALUES (%s, %s, %s, false, 0)"
            self.cursor.execute(query, (username, password, role))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")
            self.conn.rollback()
    
    def update_user(self, user_id, username, password, role, is_blocked):
        try:
            if password:
                query = "UPDATE users SET username = %s, password_hash = %s, role = %s, is_blocked = %s WHERE id = %s"
                self.cursor.execute(query, (username, password, role, is_blocked, user_id))
            else:
                query = "UPDATE users SET username = %s, role = %s, is_blocked = %s WHERE id = %s"
                self.cursor.execute(query, (username, role, is_blocked, user_id))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка обновления пользователя: {e}")
            self.conn.rollback()
    
    def delete_user(self, user_id):
        try:
            query = "DELETE FROM users WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка удаления пользователя: {e}")
            self.conn.rollback()
    
    def user_exists(self, username):
        try:
            query = "SELECT id FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"Ошибка проверки пользователя: {e}")
            self.conn.rollback()
            return False
    
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass