from fastapi import FastAPI, HTTPException

app = FastAPI()


tasks = []
task_id_counter = 1


def find_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


@app.post("/tasks/", status_code=201)
def create_task(title: str, description: str, status: str = "incomplete"):
    global task_id_counter
    new_task = {
        "id": task_id_counter,
        "title": title,
        "description": description,
        "status": status
    }
    tasks.append(new_task)
    task_id_counter += 1
    return new_task


@app.get("/tasks/")
def get_tasks(status: str = None):
    if status:
        filtered_tasks = [task for task in tasks if task["status"] == status]
        return [{"index": i, **task} for i, task in enumerate(filtered_tasks)]
    
    return [{"index": i, **task} for i, task in enumerate(tasks)]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, title: str, description: str, status: str):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task["title"] = title
    task["description"] = description
    task["status"] = status
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks = [task for task in tasks if task["id"] != task_id]
    return {"message": "Task deleted successfully"}


@app.get("/tasks/filter/")
def filter_tasks_by_status(status: str):
    if status not in ["complete", "incomplete"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    filtered_tasks = [task for task in tasks if task["status"] == status]
    return filtered_tasks