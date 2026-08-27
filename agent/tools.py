tasks = []


def create_task(title: str, description: str = "") -> dict:
    """Create a new task and add it to the task list."""
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "status": "pending",
    }

    tasks.append(task)

    return {
        "success": True,
        "task": task,
    }


def list_tasks() -> dict:
    """Return all tasks currently tracked by Taskmaster."""
    return {
        "success": True,
        "tasks": tasks,
    }


def complete_task(task_id: int, confirmation: str = "") -> dict:
    """Mark a task as completed only when the user confirms the work is actually done."""
    for task in tasks:
        if task["id"] == task_id:
            if not confirmation.strip():
                return {
                    "success": False,
                    "error": "Task cannot be completed without confirmation that the work was actually performed.",
                }
            if task["status"] == "completed":
                return {
                    "success": False,
                    "error": f"Task {task_id} is already completed.",
                }

            task["status"] = "completed"

            return {
                "success": True,
                "task": task,
            }

    return {
        "success": False,
        "error": f"Task {task_id} was not found.",
    }