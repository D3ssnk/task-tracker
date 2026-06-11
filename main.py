import os
import json
from exceptions import *
class TaskManager():
    def __init__(self,json_file = "tasks.json"):
        if not os.path.exists(json_file) or os.path.getsize(json_file) == 0:
            with open(json_file, "w") as file:
                file.write('[]')
        self.json_file = json_file
    
    def get_file(self):
        with open(self.json_file, "r") as file:
            json_data = json.load(file)
        return json_data
    
    def check_task_exists(self, json_data, id):
        if json_data == [] or id > len(json_data):
            raise TaskNotFound()

    def add(self, description):
        with open(self.json_file, "r+") as file:
            json_data = json.load(file)
            task_id = len(json_data) + 1
            task = {"id": task_id, "description": description, "status": "todo"}
            
            json_data.append(task) # appends the task to the json list
            file.seek(0) # sets the cursor to the start so you can rewrite the entire file 
            json.dump(json_data,file) # writes the data back into the file 
    
    def delete(self, id):
        json_data = self.get_file()
        
        self.check_task_exists(json_data, id)
            
        task_index = id - 1 
        del json_data[task_index]
        for n in range(task_index,len(json_data),1):
            json_data[n]['id'] -= 1
        
        with open(self.json_file, "w") as file:
            json.dump(json_data, file)

    def update(self, id, description):
        json_data = self.get_file()
        
        self.check_task_exists(json_data, id)
        
        task_index = id - 1 
        json_data[task_index]["description"] = description

        with open(self.json_file, "w") as file:
            json.dump(json_data, file)
    
    def mark(self, id, status):
        json_data = self.get_file()

        self.check_task_exists(json_data, id)

        task_index = id - 1 
        json_data[task_index]["status"] = status

        with open(self.json_file, "w") as file:
            json.dump(json_data, file)

    def list_tasks(self, status = None):
        json_data = self.get_file()
        if len(json_data) == 0:
            return "There are no tasks!"

        if status:
            json_data = [n for n in json_data if n["status"] == status]
            if len(json_data) == 0:
                return "There are no tasks with status: " + status + "!"
        
        list_string = ""
        for task in json_data:
            task_string = f"id: {task['id']}\ndescription: {task['description']}\nstatus: {task['status']}\n\n"
            list_string += task_string
        
        return list_string.strip()


def main():
    return 0

if __name__ == "__main__":
    main()
        
