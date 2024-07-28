import os
import csv
import functools
from typing import List
from tabulate import tabulate


class Task:
    def __init__(self, id: str, title: str, desc: str, weight: int):
        self.id = id
        self.title = title
        self.desc = desc
        self.weight = weight
        self.is_complete = False

    def modify_field(self, field_name, value):
        if field_name == "weight":
            value = int(value)
        setattr(self, field_name, value)

    def complete(self):
        self.is_complete = True


def before_method(decorator_func):
    """
    A decorator that runs `decorator_func` before the actual method call.
    """

    def decorator_wrapper(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            decorator_func(self)
            return method(self, *args, **kwargs)

        return wrapper

    return decorator_wrapper


def clear_terminal(self):
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print(
        """
  ______           __   ____                            
 /_  __/___ ______/ /__/ __ )___  ____ __   _____  _____
  / / / __ `/ ___/ //_/ __  / _ \/ __ `/ | / / _ \/ ___/
 / / / /_/ (__  ) ,< / /_/ /  __/ /_/ /| |/ /  __/ /    
/_/  \__,_/____/_/|_/_____/\___/\__,_/ |___/\___/_/                                            
"""
    )


class BotClient:
    def __init__(self):
        self._data: List[Task] = []
        self.active_task: Task = None
        self.welcome()

    def print_line(self):
        print("---------------------------------------------------------")

    def handle_redirect(self, fn, label):
        print(f"[{label}: 1]\n")
        action = input("Enter your selection: ")
        if action == "1":
            callable_fn = self[fn]
            callable_fn()
        else:
            print("Error command not recognized")
            self.handle_redirect(fn, label)

    @before_method(clear_terminal)
    def welcome(self, status=None):
        print("-------------------------Welcome-------------------------")
        if status:
            print("*********************************************************")
            print(status)
            print("*********************************************************")
            self.print_line()
        print(
            "\n Welcome to TaskBeaver, your go to CLI client for \n managing your productivity. This tool help you ensure \n you are always on time with your various deliverables. \n"
        )
        user_input = input("Press 1 to continue to the menu: ")
        if user_input == "1":
            self.menu()
        else:
            self.welcome("Invalid entry")

    @before_method(clear_terminal)
    def menu(self, status=None):
        newline = "\n" if not status else ""
        print(
            f"--------------------------Menu---------------------------{newline}")
        if status:
            print("*********************************************************")
            print(status)
            print("*********************************************************")
            self.print_line()
        print("1. Add new task")
        print("2. View all tasks")
        print("3. Import via CSV")
        print("4. Export via CSV")
        print("5. Exit")
        print(
            "\n Navigate through the options to interact with your tasks. \n Export tasks to reuse them in the future."
        )
        self.print_line()
        user_input = input("Enter your option number: ")
        if user_input == "1":
            self.add()
        elif user_input == "2":
            self.view()
        elif user_input == "3":
            self.import_tasks()
        elif user_input == "4":
            self.export_tasks()
        elif user_input == "5":
            print("""*********************************************************
All work will be lost unless you have exported to .csv
*********************************************************""")
            print("[Y] to confirm   [any] to cancel")
            confirm_input = input("Enter your selection: ").lower()
            if confirm_input == "y":
                print("Bye Bye :)")
                quit()
            else:
                self.menu("Exit aborted")
        else:
            self.menu("Error command not recognized")

    @before_method(clear_terminal)
    def add(self):
        print("------------------------New Task-------------------------\n")
        print("Add the following information to create a new task \n")
        title = input("Task title: ")
        desc = input("Task description: ")
        weight = input("Task priority (1-10): ")
        self.print_line()
        print("[S] to save     [R] to reset     [M] to menu")
        self.print_line()
        action = input("Enter action: ").lower()

        if action == "s":
            new_task = Task(len(self._data) + 1, title, desc, weight)
            self._data.append(new_task)
            self.menu("Task saved succesfully")
        elif action == "r":
            self.add()
        elif action == "m":
            self.menu("Task creation canceled")

    @before_method(clear_terminal)
    def view(self, status=None):
        print("-----------------------All Tasks------------------------\n")
        if status:
            print("*********************************************************")
            print(status)
            print("*********************************************************")
            self.print_line()
        if len(self._data) == 0:
            self.menu("Error, no tasks created yet")
        task_data = [
            [
                task.id,
                task.title.capitalize(),
                task.desc.capitalize(),
                task.weight,
                "✔" if task.is_complete else "✘",
            ]
            for task in self._data
        ]
        headers = ["ID", "Title", "Description", "Priority", "Status"]
        colalign = ("right", "left", "left", "center", "center")
        print(tabulate(task_data, headers, tablefmt="github", colalign=colalign))
        self.print_line()
        print("[ID] to edit     [S] to sort     [M] to menu")
        action = input("Enter your selection: ").lower()
        if action == "s":
            # sorts
            pass
        elif action == "m":
            self.menu()
        elif int(action) <= len(self._data):
            # handle edit
            self.active_task = self._data[int(action) - 1]
            self.edit()
        else:
            self.view("Command not recognized")

    @before_method(clear_terminal)
    def edit(self, status=None):
        task = self.active_task
        print(
            f"----------------------Edit Task #{task.id}  -----------------------\n")
        if status:
            print("*********************************************************")
            print(status)
            print("*********************************************************")
            self.print_line()
        print(f"Title: {task.title.capitalize()}")
        print(f"Description: {task.desc.capitalize()}")
        print(f"Priority: {task.weight}")
        print(f"Status: {'Complete' if task.is_complete else 'Incomplete'}")
        self.print_line()

        def handle_edit_actions():
            print(
                "[T] edit title [D] edit desc [P] edit priority [C] complete\n[M] to menu [V] to view [X] to delete"
            )
            action = input("Enter selection: ").lower()
            if action == "t":
                title = input("Enter new title: ")
                task.modify_field("title", title)
                self.edit("Title updated")
            elif action == "d":
                desc = input("Enter new desc: ")
                task.modify_field("desc", desc)
                self.edit("Description updated")
            elif action == "p":
                weight = input("Enter new priority rating: ")
                task.modify_field("weight", weight)
                self.edit("Priority updated")
            elif action == "c":
                print("Task cannot be uncompleted")
                confirm = input("[Y] to confirm [Any] to cancel: ").lower()
                if confirm == "y":
                    task.complete()
                    self.edit("Task Complete")
                else:
                    handle_edit_actions()
            elif action == "m":
                print("All changes will be lost")
                confirm = input("[Y] to confirm [Any] to cancel: ").lower()
                if confirm == "y":
                    self.menu("Operation abandoned")
                    return
                else:
                    handle_edit_actions()
                    return
            elif action == "v":
                self.view()
                return
            else:
                self.edit("Invalid selection")
                return

        handle_edit_actions()

    @before_method(clear_terminal)
    def import_tasks(self, status=None):
        print("-----------------------Import CSV------------------------\n")
        if status:
            print("*********************************************************")
            print(status)
            print("*********************************************************")
            self.print_line()
        print(
            "To import a CSV file, make sure it follows the structure\nprovided by the export service."
        )
        self.print_line()
        print("[C] to continue    [M] to menu")
        action = input("Enter your selection: ").lower()
        if action == "m":
            self.menu("Import aborted")
        path = input("Enter the relative path of the file to be imported: ")
        try:
            with open(path, newline="") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    task = Task(row[0], row[1], row[2], row[3])
                    self._data.append(task)
            self.view("CSV imported succesfully")
        except:
            self.import_tasks("Invalid path, try again")

    @before_method(clear_terminal)
    def export_tasks(self):
        print("----------------------Export to CSV-----------------------")
        print(
            "The export service will create a .csv file in the same \ndirectory as the main program file"
        )
        self.print_line()
        action = input("[Y] to export [Any] to cancel: ").lower()
        if action == "y":
            header = ["ID", "Title", "Description", "Priority", "Status"]
            data = [
                [task.id, task.title, task.desc, task.weight, task.is_complete]
                for task in self._data
            ]
            with open("some.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
            self.menu("CSV file saved")
        else:
            self.menu("Export operation abandoned")


if __name__ == "__main__":
    client = BotClient()
