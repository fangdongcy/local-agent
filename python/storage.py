import json
import os
from typing import List, Optional
from datetime import datetime

from models import Task

class TaskStorage:
    def __init__(self, file_path: str = 'tasks.json'):
        self.file_path = file_path
        self._ensure_file_exists()
        self._load_tasks()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def _load_tasks(self):
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            self.tasks = [Task.from_dict(task_data) for task_data in data]

    def _save_tasks(self):
        with open(self.file_path, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=2)

    def add_task(self, task: Task) -> Task:
        self.tasks.append(task)
        self._save_tasks()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def update_task(self, task_id: int, updated_task: Task) -> Optional[Task]:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks[i] = updated_task
                self._save_tasks()
                return updated_task
        return None

    def delete_task(self, task_id: int) -> bool:
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) != initial_length:
            self._save_tasks()
            return True
        return False 