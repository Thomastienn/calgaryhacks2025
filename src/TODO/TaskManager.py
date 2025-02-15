from src.TODO.Task import Task
class TaskManager:
    def __init__(self):
        """Initialize the task manager with an empty dictionary."""
        # Using the description as the key for each task.
        self.tasks = {}

    def add_task(self, description: str, date=None):
        """Create and add a new task using its description as the key.

        Returns:
            dict: The full task details if successful, otherwise an error.
        """
        if not description:
            return {"error": "Task description cannot be empty!"}

        if description in self.tasks:
            return {"error": f"Task '{description}' already exists."}

        task = Task(description, date)
        self.tasks[description] = task
        return task.to_dict()

    def toggle_task_completion(self, description: str):
        """Toggle the completion status of a task using its description.

        Returns:
            dict: The updated task details if successful, otherwise an error.
        """
        if description in self.tasks:
            return self.tasks[description].toggle_completion()
        return {"error": "Task not found"}

    def remove_task(self, description: str):
        """Remove a task using its description."""
        if description in self.tasks:
            self.tasks.pop(description)
            return {"message": f"Task '{description}' removed."}
        return {"error": "Task not found"}

    def get_tasks(self):
        """Return all tasks as a dictionary with descriptions as keys."""
        return {desc: task.to_dict() for desc, task in self.tasks.items()}