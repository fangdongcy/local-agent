from datetime import datetime
from typing import List, Optional
from models import Task
from storage import TaskStorage

class TaskManager:
    def __init__(self):
        self.storage = TaskStorage()
        self._next_id = self._get_next_id()

    def _get_next_id(self) -> int:
        tasks = self.storage.get_all_tasks()
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

    def create_task(self, title: str, description: str, due_date: Optional[datetime] = None, priority: int = 1) -> Task:
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            status="待处理",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            due_date=due_date,
            priority=priority
        )
        self._next_id += 1
        return self.storage.add_task(task)

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.storage.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        return self.storage.get_all_tasks()

    def update_task_status(self, task_id: int, new_status: str) -> Optional[Task]:
        task = self.get_task(task_id)
        if task:
            task.status = new_status
            task.updated_at = datetime.now()
            return self.storage.update_task(task_id, task)
        return None

    def update_task(self, task_id: int, title: Optional[str] = None, 
                   description: Optional[str] = None, due_date: Optional[datetime] = None,
                   priority: Optional[int] = None) -> Optional[Task]:
        task = self.get_task(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if due_date:
                task.due_date = due_date
            if priority:
                task.priority = priority
            task.updated_at = datetime.now()
            return self.storage.update_task(task_id, task)
        return None

    def delete_task(self, task_id: int) -> bool:
        return self.storage.delete_task(task_id)

    def get_tasks_by_status(self, status: str) -> List[Task]:
        return [task for task in self.get_all_tasks() if task.status == status]

    def get_tasks_by_priority(self, priority: int) -> List[Task]:
        return [task for task in self.get_all_tasks() if task.priority == priority] 