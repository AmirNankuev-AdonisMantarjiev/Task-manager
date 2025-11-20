import json
from Console import save_tasks, load_tasks, view_tasks, delete_task

def test_load_tasks_file_not_exist(tmp_path):
    filename = tmp_path / "non_existent.json"
    result = load_tasks(filename)
    assert result == []

def test_load_tasks_valid_json(tmp_path):
    filename = tmp_path / "tasks.json"
    data = [{"title": "Task 1", "priority": "High"}]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f)
    result = load_tasks(filename)
    assert result == data

def test_load_tasks_invalid_json(tmp_path):
    filename = tmp_path / "tasks.json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("not a json")
    result = load_tasks(filename)
    assert result == []

def test_save_tasks_creates_file_and_writes_correct_data(tmp_path):
    filename = tmp_path / "tasks.json"
    tasks = [{"title": "Test Task", "priority": "Low"}]

    save_tasks(tasks, filename)

    assert filename.exists()

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == tasks

def test_save_tasks_overwrites_file(tmp_path):
    filename = tmp_path / "tasks.json"
    initial_data = [{"title": "Old Task", "priority": "High"}]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(initial_data, f)

    tasks = [{"title": "New Task", "priority": "Medium"}]
    save_tasks(tasks, filename)

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == tasks

def test_view_tasks(capsys):
    tasks_empty = []
    view_tasks(tasks_empty)
    captured = capsys.readouterr()
    assert "Список задач пуст." in captured.out

    tasks = [
        {"title": "Купить хлеб", "priority": "Средний"},
        {"title": "Поспать", "priority": "Высокий"}
    ]
    view_tasks(tasks)
    captured = capsys.readouterr()
    assert "1, Купить хлеб- Средний" in captured.out
    assert "2, Поспать- Высокий" in captured.out

from unittest.mock import patch
from Console import add_task

def test_add_task(monkeypatch):
    tasks = []

    inputs = iter(["Моя задача", "Высокий"])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('Console.save_tasks') as mock_save:
        add_task(tasks)

    mock_save.assert_called_once_with(tasks)

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Моя задача"
    assert tasks[0]["priority"] == "Высокий"

    def test_delete_task(tasks):
        def test_delete_task_empty_list(capsys):
            tasks = []
            delete_task(tasks)
            captured = capsys.readouterr()
            assert "Нет задач для удаления." in captured.out

        def test_delete_task_non_empty_list(capsys):
            tasks = [{"title": "Test Task", "priority": "High"}]
            delete_task(tasks)
            # Здесь добавьте дополнительные проверки, если функция delete_task должна изменять список
            captured = capsys.readouterr()
            # Если delete_task что-то печатает при удалении, проверьте вывод, иначе пропустите
            # Пример:
            # assert "Удалена задача" in captured.out или подобное
            assert len(tasks) == 1  # если в вашей функции нет удаления, проверяем что список не изменился