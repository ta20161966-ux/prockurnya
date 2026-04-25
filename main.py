import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json
import os

# --- Настройки ---
FAVORITES_FILE = "favorites.json"
GITHUB_API_URL = "https://api.github.com/users/"

# --- Загрузка избранных пользователей из файла ---
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# --- Сохранение избранных пользователей в файл ---
def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

# --- Поиск пользователя на GitHub ---
def search_user():
    username = entry_username.get().strip()
    if not username:
        messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
        return

    try:
        response = requests.get(f"{GITHUB_API_URL}{username}")
        response.raise_for_status()  # Проверка на ошибки HTTP

        user_data = response.json()
        display_user_info(user_data)

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            messagebox.showerror("Ошибка", f"Пользователь '{username}' не найден.")
        else:
            messagebox.showerror("Ошибка API", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла непредвиденная ошибка: {e}")

# --- Отображение информации о пользователе в интерфейсе ---
def display_user_info(user_data):
    # Очистка предыдущих данных
    for widget in info_frame.winfo_children():
        widget.destroy()

    # Отображение аватара (если есть)
    avatar_url = user_data.get('avatar_url')
    # Для отображения картинки в Tkinter потребуется PIL (Pillow), здесь просто ссылка

    # Отображение данных
    tk.Label(info_frame, text=f"Имя: {user_data.get('name', 'Нет данных')}", font=('Arial', 12)).pack(anchor='w')
    tk.Label(info_frame, text=f"Логин: {user_data.get('login')}", font=('Arial', 12)).pack(anchor='w')
    tk.Label(info_frame, text=f"Био: {user_data.get('bio', 'Нет данных')}", font=('Arial', 10), wraplength=300).pack(anchor='w')
    tk.Label(info_frame, text=f"Подписчики: {user_data.get('followers', 0)}", font=('Arial', 10)).pack(anchor='w')
    
    # Кнопка "В избранное"
    btn_fav = tk.Button(info_frame, text="⭐ Добавить в избранное", 
                        command=lambda data=user_data: add_to_favorites(data))
    btn_fav.pack(pady=10)

# --- Добавление пользователя в избранное ---
def add_to_favorites(user_data):
    favorites = load_favorites()
    
    # Проверка на дубликаты по логину
    if any(u['login'] == user_data['login'] for u in favorites):
        messagebox.showinfo("Информация", f"{user_data['login']} уже в избранном!")
        return

    favorites.append(user_data)
    save_favorites(favorites)
    messagebox.showinfo("Успех", f"{user_data['login']} добавлен в избранное!")

# --- Создание главного окна ---
root = tk.Tk()
root.title("GitHub User Finder")
root.geometry("450x450")
root.resizable(False, False)

# --- Верхняя часть: Поле ввода и кнопка ---
top_frame = tk.Frame(root)
top_frame.pack(pady=10, padx=10, fill='x')

tk.Label(top_frame, text="Введите логин пользователя:", font=('Arial', 12)).pack(side='left')
entry_username = tk.Entry(top_frame, font=('Arial', 12), width=25)
entry_username.pack(side='left', padx=5)
tk.Button(top_frame, text="🔍 Поиск", font=('Arial', 12), command=search_user).pack(side='left')

# --- Нижняя часть: Отображение информации ---
info_frame = tk.Frame(root)
info_frame.pack(pady=10, padx=10, fill='both', expand=True)

# --- Запуск приложения ---
if __name__ == "__main__":
    root.mainloop()
