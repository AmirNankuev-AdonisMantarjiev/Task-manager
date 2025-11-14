import json
import os

FILENAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            tasks = json.load(f)
            return tasks
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)




def view_tasks(tasks):
    if len(tasks) == 0:
        print("Список задач пуст.")
        return
    else:
        for i, task in enumerate(tasks, start=1):
            print(f"{i}, {task['title']}- {task['priority']}")

def add_task(tasks):
    title = input("Введите название задачи")
    priority = input("Введите приориет (Низкий/Средний/Высокий)")
    task = {"title": title, "priority": priority}
    tasks.append(task)
    save_tasks(tasks)
    print("Задача добавлена")



def delete_task(tasks):
    if len(tasks) == 0:
        print("Нет задач для удаления.")
        return

    view_tasks(tasks)

    number = input("Введите номер задачи: ")
    try:
        num = int(number)
    except ValueError:
        print("Пожалуйста, введите корректное число.")
        return

    if not (1 <= num <= len(tasks)):
        print("Некорректный номер задачи.")
        return

    deleted_task = tasks.pop(num - 1)
    save_tasks(tasks)
    print("Задача удалена.")



def main():
    print("Добро пожаловать в менеджер задач!")

    tasks = load_tasks()

    while True:
        print("\nМеню:")
        print("1 — Просмотреть задачи")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу")
        print("0 — Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Ошибка: такого пункта меню нет. Попробуйте снова.")


if __name__ == "__main__":
    main()