class GoogleLogger:
    def log_task(self, task_id, description, result):
        print(f"[LOGGED] Task ID: {task_id} | Description: {description} | Result: {result}")
