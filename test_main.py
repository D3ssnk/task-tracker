from main import TaskManager
from exceptions import *
import json
import pytest
import os


@pytest.fixture
def test_task_manager():
    return TaskManager("test_json.json")


@pytest.fixture
def test_empty_json_file():
    if not os.path.exists("test_json.json") or os.path.getsize("test_json.json") != 0:
        with open("test_json.json","w") as file:
            file.write('[]')

    yield "test_json.json"
    if os.path.exists("test_json.json"):
        os.remove("test_json.json")
    

def test_add(test_task_manager, test_empty_json_file):
    test_tasks = [{'id': 1, 'description': 'Make Coffee', "status": "todo"}]
    test_task_manager.add("Make Coffee")

    with open(test_empty_json_file, "r") as file:
        json_data = json.load(file)

    assert json_data == test_tasks, "Correctly adds task with ID as one"

        
    test_task_manager.add("Make Tea")
    test_tasks.append({'id': 2, 'description': 'Make Tea', "status": "todo"})

    with open(test_empty_json_file, "r") as file:
        json_data = json.load(file)

    assert json_data == test_tasks, "Correctly adds task with incremented ID"


@pytest.fixture
def test_json_file():
    test_tasks = [{'id': 1, 'description': 'Make Coffee', "status": "todo"}, {'id': 2, 'description': 'Make Tea', "status": "in-progress"}, {'id': 3, 'description': 'Make Soup', "status": "done"}]
    if not os.path.exists("test_json.json") or os.path.getsize("test_json.json") != 0:
        with open("test_json.json","w") as file:
            json.dump(test_tasks, file)

    yield "test_json.json"
    if os.path.exists("test_json.json"):
        os.remove("test_json.json")


def test_get_file(test_task_manager, test_json_file):
    with open(test_json_file,'r') as file:
        json_data = json.load(file)
    
    assert test_task_manager.get_file() == json_data

def test_check_task_exists(test_task_manager, test_json_file):
    with open(test_json_file,'r') as file:
        json_data = json.load(file)
    
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.check_task_exists(json_data, 6)

def test_delete(test_task_manager, test_json_file):
    # test that when you delete a task, it gets deleted and also updates later tasks
    test_task_manager.delete(1)
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Tea', "status": "in-progress"}, {'id': 2, 'description': 'Make Soup', "status": "done"}], "Ensure task was deleted and next task was updated"

    # test that when you try to delete a task with the wrong id, it throws an exception
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.delete(4)

    # test that when you delete the last task the file is an empty list and not empty
    test_task_manager.delete(1)
    test_task_manager.delete(1)
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [], "Ensure task was deleted file is an empty list"

    # test that when you try to delete a task with no tasks inside the file it throws an exception
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.delete(1)

    
def test_update(test_task_manager, test_json_file):
    # test that when you update a task, the task gets updated
    test_task_manager.update(1, "Make Water")
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Water', "status": "todo"}, {'id': 2, 'description': 'Make Tea', "status": "in-progress"}, {'id': 3, 'description': 'Make Soup', "status": "done"}], "Ensure task was updated and the rest remain the same"

    # test that when you update a task, the task gets updated, but consecutively
    test_task_manager.update(2, "Make Water")
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Water', "status": "todo"}, {'id': 2, 'description': 'Make Water', "status": "in-progress"}, {'id': 3, 'description': 'Make Soup', "status": "done"}], "Ensure task was updated and the rest remain the same"

    # test that when you try to update a task with the wrong id, it throws an exception
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.update(4, "Make Water")

    # test that when you try to update a task with no tasks inside the file it throws an exception
    with open("test_json.json","w") as file:
            file.write('[]')
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.update(1, "Make Water")

def test_mark(test_task_manager, test_json_file):
    # test that when you mark as done, the task gets marked as done
    test_task_manager.mark(1, "done")
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Coffee', "status": "done"}, {'id': 2, 'description': 'Make Tea', "status": "in-progress"}, {'id': 3, 'description': 'Make Soup', "status": "done"}], "Ensure task was marked done and the rest remain the same"

    # test that when you mark as todo, the task gets marked as todo
    test_task_manager.mark(2, "todo")
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Coffee', "status": "done"}, {'id': 2, 'description': 'Make Tea', "status": "todo"}, {'id': 3, 'description': 'Make Soup', "status": "done"}], "Ensure task was marked todo and the rest remain the same"

    # test that when you mark as in-progress, the task gets marked as in-progress
    test_task_manager.mark(3, "in-progress")
    with open(test_json_file, "r") as file:
        json_data = json.load(file)
    assert json_data == [{'id': 1, 'description': 'Make Coffee', "status": "done"}, {'id': 2, 'description': 'Make Tea', "status": "todo"}, {'id': 3, 'description': 'Make Soup', "status": "in-progress"}], "Ensure task was marked in-progress and the rest remain the same"

    # test that when you try to mark a task with the wrong id, it throws an exception (done)
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.update(4, "done")
    
    # test that when you try to mark a task with the wrong id, it throws an exception 
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.update(4, "todo")
        test_task_manager.update(4, "in-progress")
        test_task_manager.update(4, "done")

    # test that when you try to update a task with no tasks inside the file it throws an exception
    with open("test_json.json","w") as file:
            file.write('[]')
    with pytest.raises(TaskNotFound, match = "This task does not exist" ):
        test_task_manager.update(4, "todo")
        test_task_manager.update(4, "in-progress")
        test_task_manager.update(4, "done")
