import json
import os
from datetime import datetime

class BookManager:
    def __init__(self, filename="books.json"):
        self.filename = filename
        self.books = []
        self.load_books()
    
    def load_books(self):
        """Загрузка книг из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.books = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.books = []
        else:
            self.books = []
    
    def save_books(self):
        """Сохранение книг в JSON файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)
    
    def add_book(self, title, author, genre, pages):
        """Добавление новой книги"""
        # Проверка на дубликаты (книга с таким же названием и автором)
        for book in self.books:
            if book["title"].lower() == title.lower() and book["author"].lower() == author.lower():
                return False, "Книга с таким названием и автором уже существует!"
        
        book = {
            "title": title.strip(),
            "author": author.strip(),
            "genre": genre.strip(),
            "pages": int(pages),
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Прочитана"
        }
        self.books.append(book)
        self.save_books()
        return True, "Книга добавлена!"
    
    def get_all_books(self):
        """Получение всех книг"""
        return self.books
    
    def filter_by_genre(self, genre):
        """Фильтрация по жанру"""
        if genre == "Все":
            return self.books
        return [b for b in self.books if b["genre"] == genre]
    
    def filter_by_pages(self, min_pages):
        """Фильтрация по количеству страниц (больше указанного)"""
        return [b for b in self.books if b["pages"] > min_pages]
    
    def delete_book(self, title, author):
        """Удаление книги по названию и автору"""
        original_count = len(self.books)
        self.books = [b for b in self.books if not (b["title"] == title and b["author"] == author)]
        if len(self.books) < original_count:
            self.save_books()
            return True
        return False
    
    def get_unique_genres(self):
        """Получение списка уникальных жанров"""
        genres = list(set([book["genre"] for book in self.books]))
        return ["Все"] + sorted(genres)
    
    def search_books(self, keyword):
        """Поиск книг по названию или автору"""
        keyword_lower = keyword.lower()
        return [b for b in self.books if keyword_lower in b["title"].lower() or keyword_lower in b["author"].lower()]