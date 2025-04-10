import sys
from datetime import datetime
from task_manager import TaskManager

class TaskCLI:
    def __init__(self):
        self.task_manager = TaskManager()

    def display_menu(self):
        print("\n=== 任务管理系统 ===")
        print("1. 创建新任务")
        print("2. 查看所有任务")
        print("3. 查看特定任务")
        print("4. 更新任务状态")
        print("5. 更新任务信息")
        print("6. 删除任务")
        print("7. 按状态查看任务")
        print("8. 按优先级查看任务")
        print("0. 退出")
        print("================")

    def create_task(self):
        title = input("请输入任务标题: ")
        description = input("请输入任务描述: ")
        due_date_str = input("请输入截止日期 (YYYY-MM-DD，可选): ")
        priority = int(input("请输入优先级 (1-低, 2-中, 3-高): "))

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

        task = self.task_manager.create_task(title, description, due_date, priority)
        print(f"任务已创建，ID: {task.id}")

    def list_tasks(self):
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("没有任务")
            return

        print("\n所有任务:")
        for task in tasks:
            self._display_task(task)

    def view_task(self):
        task_id = int(input("请输入任务ID: "))
        task = self.task_manager.get_task(task_id)
        if task:
            self._display_task(task)
        else:
            print("任务不存在")

    def update_task_status(self):
        task_id = int(input("请输入任务ID: "))
        print("可选状态: 待处理、进行中、已完成、已取消")
        new_status = input("请输入新状态: ")
        
        task = self.task_manager.update_task_status(task_id, new_status)
        if task:
            print("状态已更新")
        else:
            print("任务不存在")

    def update_task_info(self):
        task_id = int(input("请输入任务ID: "))
        title = input("请输入新标题 (直接回车保持不变): ")
        description = input("请输入新描述 (直接回车保持不变): ")
        due_date_str = input("请输入新截止日期 (YYYY-MM-DD，直接回车保持不变): ")
        priority_str = input("请输入新优先级 (1-3，直接回车保持不变): ")

        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")

        priority = None
        if priority_str:
            priority = int(priority_str)

        task = self.task_manager.update_task(task_id, title or None, 
                                           description or None, 
                                           due_date, 
                                           priority)
        if task:
            print("任务已更新")
        else:
            print("任务不存在")

    def delete_task(self):
        task_id = int(input("请输入要删除的任务ID: "))
        if self.task_manager.delete_task(task_id):
            print("任务已删除")
        else:
            print("任务不存在")

    def list_tasks_by_status(self):
        print("可选状态: 待处理、进行中、已完成、已取消")
        status = input("请输入状态: ")
        tasks = self.task_manager.get_tasks_by_status(status)
        if tasks:
            print(f"\n状态为 '{status}' 的任务:")
            for task in tasks:
                self._display_task(task)
        else:
            print(f"没有状态为 '{status}' 的任务")

    def list_tasks_by_priority(self):
        priority = int(input("请输入优先级 (1-低, 2-中, 3-高): "))
        tasks = self.task_manager.get_tasks_by_priority(priority)
        if tasks:
            print(f"\n优先级为 {priority} 的任务:")
            for task in tasks:
                self._display_task(task)
        else:
            print(f"没有优先级为 {priority} 的任务")

    def _display_task(self, task):
        print(f"\nID: {task.id}")
        print(f"标题: {task.title}")
        print(f"描述: {task.description}")
        print(f"状态: {task.status}")
        print(f"创建时间: {task.created_at}")
        print(f"更新时间: {task.updated_at}")
        if task.due_date:
            print(f"截止日期: {task.due_date}")
        print(f"优先级: {task.priority}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("请选择操作 (0-8): ")

            try:
                if choice == "1":
                    self.create_task()
                elif choice == "2":
                    self.list_tasks()
                elif choice == "3":
                    self.view_task()
                elif choice == "4":
                    self.update_task_status()
                elif choice == "5":
                    self.update_task_info()
                elif choice == "6":
                    self.delete_task()
                elif choice == "7":
                    self.list_tasks_by_status()
                elif choice == "8":
                    self.list_tasks_by_priority()
                elif choice == "0":
                    print("感谢使用！再见！")
                    sys.exit(0)
                else:
                    print("无效的选择，请重试")
            except ValueError as e:
                print(f"输入错误: {e}")
            except Exception as e:
                print(f"发生错误: {e}")

if __name__ == "__main__":
    cli = TaskCLI()
    cli.run() 