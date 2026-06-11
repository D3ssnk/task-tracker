from main import TaskManager
from exceptions import *
import json
import pytest
import os


@pytest.fixture
def test_task_manager(test_json_file):
    return TaskManager(test_json_file)


@pytest.fixture
def test_json_file():
    if not os.path.exists("test_json.json") or os.path.getsize("test_json.json") != 0:
        with open("test_json.json","w") as file:
            file.write('[]')

    yield "test_json.json"
    if os.path.exists("test_json.json"):
        os.remove("test_json.json")
    



def test_add(test_task_manager, test_json_file):
    test_tasks = [{'id': 1, 'description': 'Make Coffee', "status": "todo"}]
    test_task_manager.add("Make Coffee")

    with open(test_json_file, "r") as file:
        json_data = json.load(file)

    assert json_data == test_tasks, "Correctly adds task with ID as one"

        
    test_task_manager.add("Make Tea")
    test_tasks.append({'id': 2, 'description': 'Make Tea', "status": "todo"})

    with open(test_json_file, "r") as file:
        json_data = json.load(file)

    assert json_data == test_tasks, "Correctly adds task with incremented ID"


def test_delete(test_task_manager, test_json_file):
    test_tasks = [{'id': 1, 'description': 'Make Coffee', "status": "todo"}, {'id': 2, 'description': 'Make Tea', "status": "todo"}]
    with open(test_json_file, "r+") as file:
        json_data = json.load(file)
        json_data += test_tasks
        file.seek(0)
        json.dump(json_data, file)
    
    # test that when you delete a task, it gets deleted and also updates later tasks
    test_task_manager.delete(1)
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Tea', "status": "todo"}], "Ensure task was deleted and next task was updated"

    # test that when you try to delete a task with the wrong id, it throws an exception
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.delete(2)

    # test that when you delete the last task the file is an empty list and not empty
    test_task_manager.delete(1)
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [], "Ensure task was deleted file is an empty list"

    # test that when you try to delete a task with no tasks inside it throws an exception
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.delete(2)

    
