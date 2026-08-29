from google.cloud import firestore


PROJECT_ID = "gen-lang-client-0349849444"
DATABASE_ID = "taskflow-db"
COLLECTION_NAME = "tasks"

db = firestore.Client(
    project=PROJECT_ID,
    database=DATABASE_ID,
)

tasks_collection = db.collection(COLLECTION_NAME)


def create_task(title: str, description: str = "") -> dict:
    """Create a new task in Firestore."""

    existing_tasks = list(tasks_collection.stream())

    task_id = max(
        (
            doc.to_dict().get("id", 0)
            for doc in existing_tasks
        ),
        default=0,
    ) + 1

    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": "pending",
    }

    tasks_collection.document(str(task_id)).set(task)

    return {
        "success": True,
        "task": task,
    }


def list_tasks() -> dict:
    """Return all tasks currently tracked by Taskmaster."""

    documents = tasks_collection.stream()

    tasks = [doc.to_dict() for doc in documents]
    tasks.sort(key=lambda task: task.get("id", 0))

    return {
        "success": True,
        "tasks": tasks,
    }


def start_task(task_id: int) -> dict:
    """Mark a pending task as in progress."""

    task_ref = tasks_collection.document(str(task_id))
    task_snapshot = task_ref.get()

    if not task_snapshot.exists:
        return {
            "success": False,
            "error": f"Task {task_id} was not found.",
        }

    task = task_snapshot.to_dict()

    if task["status"] == "completed":
        return {
            "success": False,
            "error": f"Task {task_id} is already completed.",
        }

    if task["status"] == "in_progress":
        return {
            "success": False,
            "error": f"Task {task_id} is already in progress.",
        }

    task["status"] = "in_progress"
    task_ref.set(task)

    return {
        "success": True,
        "task": task,
    }


def complete_task(task_id: int, confirmation: str = "") -> dict:
    """Mark a task as completed only when confirmation is provided."""

    if not confirmation.strip():
        return {
            "success": False,
            "error": (
                "Task cannot be completed without confirmation "
                "that the work was actually performed."
            ),
        }

    task_ref = tasks_collection.document(str(task_id))
    task_snapshot = task_ref.get()

    if not task_snapshot.exists:
        return {
            "success": False,
            "error": f"Task {task_id} was not found.",
        }

    task = task_snapshot.to_dict()

    if task["status"] == "completed":
        return {
            "success": False,
            "error": f"Task {task_id} is already completed.",
        }

    task["status"] = "completed"
    task_ref.set(task)

    return {
        "success": True,
        "task": task,
    }