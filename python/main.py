#!/usr/bin/env python3
from cli import TaskCLI

def main():
    print("欢迎使用任务管理系统！")
    cli = TaskCLI()
    cli.run()

if __name__ == "__main__":
    main() 