class Task:
    def __init__(self, description, date=None):
        """Initialize a single task with an optional date."""
        self.description = description
        self.date = date
        self.completed = False

    def mark_completed(self):
        """Mark the task as completed and return the updated task as a dict."""
        self.completed = True
        return self.to_dict()

    def toggle_completion(self):
        """Toggle the task's completion status and return the updated task as a dict."""
        self.completed = not self.completed
        return self.to_dict()

    def to_dict(self):
        """Return the task data as a dictionary."""
        return {
            "task": self.description,
            "date": self.date,
            "completed": self.completed
        }