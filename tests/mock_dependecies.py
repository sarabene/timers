from app.database import Database
from app.job_queue import JobQueue
from app.models import Timer


class Mock_DB(Database):
    def __init__(self, timers: dict):
        self.timers = timers

    def save_timer(self, timer: Timer):
        self.timers.update({str(timer.id): timer})

    def get_timer(self, timer_id: str):
        timer_in_db = self.timers.get(timer_id)
        return timer_in_db


class Mock_RQ(JobQueue):
    def __init__(self, jobs: list):
        self.jobs = jobs

    def schedule_job_for_timer(self, timer: Timer):
        job = (timer.timestamp, timer.id)
        self.jobs.append(job)
