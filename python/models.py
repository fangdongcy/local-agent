from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    priority: int = 1  # 1: 低, 2: 中, 3: 高

    def __post_init__(self):
        # Bug 1: 没有验证priority的范围，允许了无效的优先级值
        if self.priority < 1 or self.priority > 3:
            self.priority = 1  # 这里应该抛出异常而不是静默修改

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        # Bug 2: 没有处理缺失字段的情况，可能导致KeyError
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=data['status'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            due_date=datetime.fromisoformat(data['due_date']) if data['due_date'] else None,
            priority=data['priority']
        ) 