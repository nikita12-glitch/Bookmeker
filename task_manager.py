import json
import os
import random
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Загрузка задач из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Сохранение задач в JSON файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)
    
    def add_task(self, title, description, priority="Средний"):
        """Добавление новой задачи с уникальным ID"""
        task = {
            "id": random.randint(1000, 9999),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "Активна",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_all_tasks(self):
        return self.tasks
    
    def filter_by_priority(self, priority):
        """Фильтрация задач по приоритету"""
        return [t for t in self.tasks if t["priority"] == priority]
    
    def filter_by_status(self, status):
        """Фильтрация задач по статусу"""
        return [t for t in self.tasks if t["status"] == status]
    
    def delete_task(self, task_id):
        """Удаление задачи по ID"""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save_tasks()
    
    def update_status(self, task_id, new_status):
        """Обновление статуса задачи"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                self.save_tasks()
                return True
        return False
    
    def search_by_title(self, keyword):
        """Поиск задач по названию"""
        keyword_lower = keyword.lower()
        return [t for t in self.tasks if keyword_lower in t["title"].lower()]