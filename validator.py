class TaskValidator:
    @staticmethod
    def validate_title(title):
        """Проверка названия задачи"""
        if not title or not isinstance(title, str):
            return False, "Название не может быть пустым"
        if len(title.strip()) == 0:
            return False, "Название не может состоять только из пробелов"
        if len(title) > 100:
            return False, "Название не должно превышать 100 символов"
        return True, "OK"
    
    @staticmethod
    def validate_description(description):
        """Проверка описания"""
        if description and len(description) > 500:
            return False, "Описание не должно превышать 500 символов"
        return True, "OK"
    
    @staticmethod
    def validate_priority(priority):
        """Проверка приоритета"""
        valid_priorities = ["Высокий", "Средний", "Низкий"]
        if priority not in valid_priorities:
            return False, f"Приоритет должен быть одним из: {valid_priorities}"
        return True, "OK"
    
    @staticmethod
    def validate_task_id(task_id):
        """Проверка ID задачи"""
        try:
            tid = int(task_id)
            return True, tid
        except ValueError:
            return False, "ID должен быть числом"