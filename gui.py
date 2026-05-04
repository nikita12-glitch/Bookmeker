import tkinter as tk
from tkinter import ttk, messagebox
from book_manager import BookManager

class BookTrackerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📚 Book Tracker - Трекер книг")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        
        # Устанавливаем иконку (опционально)
        try:
            self.root.iconbitmap(default='book.ico')
        except:
            pass
        
        self.book_manager = BookManager()
        
        self.setup_ui()
        self.refresh_book_list()
        self.update_genre_filter()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка веса для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ - ДОБАВЛЕНИЕ КНИГ =====
        left_frame = ttk.LabelFrame(main_frame, text="➕ Добавить новую книгу", padding="15")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Название
        ttk.Label(left_frame, text="Название книги:*", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.title_entry = ttk.Entry(left_frame, width=35, font=("Arial", 10))
        self.title_entry.grid(row=0, column=1, pady=8, padx=10)
        
        # Автор
        ttk.Label(left_frame, text="Автор:*", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.author_entry = ttk.Entry(left_frame, width=35, font=("Arial", 10))
        self.author_entry.grid(row=1, column=1, pady=8, padx=10)
        
        # Жанр
        ttk.Label(left_frame, text="Жанр:*", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=8)
        self.genre_var = tk.StringVar()
        self.genre_entry = ttk.Combobox(left_frame, textvariable=self.genre_var, width=32, font=("Arial", 10))
        self.genre_entry['values'] = ('Роман', 'Детектив', 'Фантастика', 'Наука', 'Поэзия', 'Биография', 'Другое')
        self.genre_entry.grid(row=2, column=1, pady=8, padx=10)
        
        # Количество страниц
        ttk.Label(left_frame, text="Количество страниц:*", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, pady=8)
        self.pages_entry = ttk.Entry(left_frame, width=35, font=("Arial", 10))
        self.pages_entry.grid(row=3, column=1, pady=8, padx=10)
        
        # Кнопка добавления
        add_btn = ttk.Button(left_frame, text="📖 Добавить книгу", command=self.add_book, width=25)
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Информация о полях
        info_label = ttk.Label(left_frame, text="* - обязательные поля", foreground="gray")
        info_label.grid(row=5, column=0, columnspan=2)
        
        # ===== ПРАВАЯ ПАНЕЛЬ - СПИСОК КНИГ =====
        right_frame = ttk.LabelFrame(main_frame, text="📋 Список прочитанных книг", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Панель фильтров
        filter_frame = ttk.Frame(right_frame)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Фильтр по жанру
        ttk.Label(filter_frame, text="Фильтр по жанру:").pack(side=tk.LEFT, padx=5)
        self.filter_genre_var = tk.StringVar(value="Все")
        self.filter_genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var, width=15, state="readonly")
        self.filter_genre_combo.pack(side=tk.LEFT, padx=5)
        self.filter_genre_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Фильтр по страницам
        ttk.Label(filter_frame, text="Страниц >").pack(side=tk.LEFT, padx=5)
        self.filter_pages_entry = ttk.Entry(filter_frame, width=8)
        self.filter_pages_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="🔍 Применить", command=self.apply_filters, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="🔄 Сброс", command=self.reset_filters, width=8).pack(side=tk.LEFT, padx=5)
        
        # Поиск
        search_frame = ttk.Frame(right_frame)
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(search_frame, text="🔎 Поиск:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Найти", command=self.search_books, width=10).pack(side=tk.LEFT, padx=5)
        
        # Таблица книг
        columns = ("Название", "Автор", "Жанр", "Страницы", "Дата добавления", "Статус")
        self.book_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=18)
        
        # Настройка заголовков и ширины колонок
        col_widths = {"Название": 200, "Автор": 150, "Жанр": 100, "Страницы": 80, "Дата добавления": 130, "Статус": 80}
        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=col_widths.get(col, 100))
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.book_tree.yview)
        self.book_tree.configure(yscrollcommand=scrollbar.set)
        
        self.book_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки управления
        control_frame = ttk.Frame(right_frame)
        control_frame.grid(row=3, column=0, pady=10)
        
        ttk.Button(control_frame, text="🗑 Удалить выбранную", command=self.delete_book, width=18).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="📊 Статистика", command=self.show_stats, width=15).pack(side=tk.LEFT, padx=5)
        
        # Настройка веса для растягивания таблицы
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
    
    def add_book(self):
        """Добавление книги с валидацией"""
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_var.get()
        pages = self.pages_entry.get()
        
        # Валидация 1: проверка на пустые поля
        if not title.strip():
            messagebox.showerror("Ошибка", "Название книги не может быть пустым!")
            return
        
        if not author.strip():
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        
        if not genre.strip():
            messagebox.showerror("Ошибка", "Выберите жанр!")
            return
        
        # Валидация 2: количество страниц - число
        try:
            pages_int = int(pages)
            if pages_int <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть больше 0!")
                return
            if pages_int > 10000:
                messagebox.showerror("Ошибка", "Количество страниц не может превышать 10000!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return
        
        # Добавление книги
        success, message = self.book_manager.add_book(title, author, genre, pages_int)
        
        if success:
            messagebox.showinfo("Успех", message)
            # Очистка полей
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.genre_entry.set('')
            self.pages_entry.delete(0, tk.END)
            # Обновление списка
            self.refresh_book_list()
            self.update_genre_filter()
        else:
            messagebox.showerror("Ошибка", message)
    
    def refresh_book_list(self, books=None):
        """Обновление таблицы книг"""
        # Очистка таблицы
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        if books is None:
            books = self.book_manager.get_all_books()
        
        # Заполнение таблицы
        for book in books:
            self.book_tree.insert("", tk.END, values=(
                book["title"],
                book["author"],
                book["genre"],
                book["pages"],
                book["added_date"],
                book["status"]
            ))
    
    def apply_filters(self):
        """Применение фильтров"""
        books = self.book_manager.get_all_books()
        
        # Фильтр по жанру
        genre_filter = self.filter_genre_var.get()
        if genre_filter != "Все":
            books = [b for b in books if b["genre"] == genre_filter]
        
        # Фильтр по страницам
        pages_filter = self.filter_pages_entry.get()
        if pages_filter:
            try:
                min_pages = int(pages_filter)
                if min_pages > 0:
                    books = [b for b in books if b["pages"] > min_pages]
            except ValueError:
                pass  # Если не число - игнорируем
        
        self.refresh_book_list(books)
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_genre_var.set("Все")
        self.filter_pages_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.refresh_book_list()
    
    def update_genre_filter(self):
        """Обновление списка жанров в фильтре"""
        genres = self.book_manager.get_unique_genres()
        self.filter_genre_combo['values'] = genres
    
    def search_books(self):
        """Поиск книг"""
        keyword = self.search_entry.get().strip()
        if keyword:
            results = self.book_manager.search_books(keyword)
            self.refresh_book_list(results)
            if not results:
                messagebox.showinfo("Результат", f"Книги по запросу '{keyword}' не найдены")
        else:
            messagebox.showwarning("Внимание", "Введите текст для поиска")
    
    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.book_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите книгу для удаления")
            return
        
        # Получение данных выбранной книги
        values = self.book_tree.item(selected[0])["values"]
        title = values[0]
        author = values[1]
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", f"Удалить книгу '{title}' (автор: {author})?"):
            if self.book_manager.delete_book(title, author):
                messagebox.showinfo("Успех", "Книга удалена")
                self.refresh_book_list()
                self.update_genre_filter()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить книгу")
    
    def show_stats(self):
        """Показать статистику"""
        books = self.book_manager.get_all_books()
        
        if not books:
            messagebox.showinfo("Статистика", "Нет добавленных книг")
            return
        
        total_books = len(books)
        total_pages = sum(book["pages"] for book in books)
        avg_pages = total_pages // total_books
        
        # Статистика по жанрам
        genres_count = {}
        for book in books:
            genre = book["genre"]
            genres_count[genre] = genres_count.get(genre, 0) + 1
        
        most_common_genre = max(genres_count, key=genres_count.get)
        
        # Формирование сообщения
        stats_text = f"""
📊 СТАТИСТИКА ПРОЧИТАННЫХ КНИГ

📚 Всего книг: {total_books}
📖 Всего страниц: {total_pages}
📏 Среднее кол-во страниц: {avg_pages}
🎭 Самый популярный жанр: {most_common_genre} ({genres_count[most_common_genre]} книг)

📈 Распределение по жанрам:
"""
        for genre, count in sorted(genres_count.items(), key=lambda x: x[1], reverse=True):
            stats_text += f"\n   • {genre}: {count} книг"
        
        messagebox.showinfo("Статистика", stats_text)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()
