import asyncio
from typing import Dict
from datetime import datetime, timedelta

class ScrapingTaskManager:
    """
    Manages background scraping tasks with status tracking
    """
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.tasks = {}
        return cls._instance
    
    def start_task(self, task_id: str, city: str):
        """
        Start a new scraping task
        """
        self.tasks[task_id] = {
            'city': city,
            'status': 'in_progress',
            'started_at': datetime.now(),
            'completed': False,
            'html_file': f"{city.lower()}_booking.html"
        }
    
    def complete_task(self, task_id: str):
        """
        Mark a task as completed
        """
        if task_id in self.tasks:
            self.tasks[task_id]['status'] = 'completed'
            self.tasks[task_id]['completed'] = True
    
    def get_task_status(self, task_id: str):
        """
        Get the status of a specific task
        """
        return self.tasks.get(task_id, {})
    
    def cleanup_old_tasks(self, max_age_minutes: int = 30):
        """
        Remove tasks older than specified time
        """
        current_time = datetime.now()
        expired_tasks = [
            task_id for task_id, task_info in self.tasks.items()
            if current_time - task_info['started_at'] > timedelta(minutes=max_age_minutes)
        ]
        for task_id in expired_tasks:
            del self.tasks[task_id]

# Global task manager instance
scraping_task_manager = ScrapingTaskManager()
