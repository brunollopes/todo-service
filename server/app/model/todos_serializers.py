
def boardEntity(board) -> dict:
    return {
        "id": board["id"],
        "name": board["name"],
        "description": board["description"],
        "createdAt": board["createdAt"],
        "updatedAt": board["updatedAt"],
        "tasks": board["tasks"]
    }
    

# def boardEntityWithTasks(board,tasks) -> dict:
#     return {
#         "id": board["id"],
#         "name": board["name"],
#         "description": board["description"],
#         "createdAt": board["createdAt"],
#         "updatedAt": board["updatedAt"],
#         "tasks": tasks
#     }


def boardListEntity(boards) -> list:
    return [boardEntity(board) for board in boards]

def taskEntity(task) -> dict:
    return {
        "id": task["id"],
        "name": task["name"],
        "description": task["description"],
        "user": task["user"],
        "status": task["status"],
        "board": task["board"],
        "createdAt": task["createdAt"],
        "updatedAt": task["updatedAt"],
        "userData": task["userData"]
    }


def taskListEntity(tasks) -> list:
    return [taskEntity(task) for task in tasks]
