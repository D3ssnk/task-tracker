import os
import json
from exceptions import *
class TaskManager():
    def __init__(self,json_file):
        if not os.path.exists(json_file) or os.path.getsize(json_file) == 0:
            with open(json_file, "w") as file:
                file.write('[]')
        self.json_file = json_file

    def add(self, task_description):
        with open(self.json_file, "r+") as file:
            json_data = json.load(file)
            task_id = len(json_data) + 1
            task = {"id": task_id, "description": task_description}
            
            json_data.append(task) # appends the task to the json list
            file.seek(0) # sets the cursor to the start so you can rewrite the entire file 
            json.dump(json_data,file) # writes the data back into the file 
    
    def delete(self, id):
        with open(self.json_file, "r") as file:
            json_data = json.load(file)
        
        if json_data == [] or id > len(json_data):
            raise TaskNotFound()
            
        task_index = id - 1 
        del json_data[task_index]
        for n in range(task_index,len(json_data),1):
            json_data[n]['id'] -= 1
        
        with open(self.json_file, "w") as file:
            json.dump(json_data, file)

            

"""

[1,2,3] 2
0,1,2
del id -1
[1,3]
0,1
from id - 1 to end: -1 
[1,2]

[1,2,3,4,5,6,7,] 3
0,1,2,3,4,5,6

del ID - 1 = 2
[1,2,4,5,6,7]
0,1,2,3,4,5
from 2 to end of list -1:

"""

def main():
    return 0

if __name__ == "__main__":
    main()
        
