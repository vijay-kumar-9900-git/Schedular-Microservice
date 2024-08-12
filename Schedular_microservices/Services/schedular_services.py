from datetime import datetime

import psycopg2
from db_connection import get_db_connection
from queries import create_job_query, get_jobs_query, get_job_query,update_last_run,update_next_run
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from croniter import croniter
from datetime import datetime

logging.basicConfig( filename='scheduler.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JobService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        logging.info("Scheduler started.")

    def create_job(self,payload):
        conn = get_db_connection()
        name=payload['name']
        interval=payload['interval']
        job_details=payload['job_details']
        print(payload)
        try:
            with conn.cursor() as cur:
                cur.execute(create_job_query, (name, interval, job_details))
                job_id = cur.fetchone()[0]
                conn.commit()
        finally:
            conn.close()

        cron_parts = interval.split(' ')
        if len(cron_parts) == 5:  # Cron-like format
            trigger = CronTrigger(
                minute=cron_parts[0],
                hour=cron_parts[1],
                day=cron_parts[2],
                month=cron_parts[3],
                day_of_week=cron_parts[4]
            )
        else:  # Default to interval trigger in minutes
            trigger = CronTrigger(minute='*/' + interval)

        self.scheduler.add_job(
            self.execute_job,
            trigger,
            args=[job_id, job_details],
            id=str(job_id)
        )
        logging.info(f"Job {job_id} scheduled with interval: {interval}")
        return {"id": job_id}

    def get_jobs(self):
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(get_jobs_query)
                jobs = cur.fetchall()
        finally:
            conn.close()
        return jobs

    def get_job(self, payload):
        job_id=payload['job_id']
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(get_job_query, (job_id,))
                job = cur.fetchone()
        finally:
            conn.close()
        return job

    def execute_job(self, job_id, job_details):
        conn = get_db_connection()
        logging.info(f"Executing job {job_id} with details: {job_details}")
        self.perform_number_crunching(job_id, job_details)
        try:
            with conn.cursor() as cur:
                cur.execute(update_last_run, (datetime.now(), job_id))
                conn.commit()
        finally:
            conn.close()
        self.update_next_run(job_id)
    # def get_next_run_time(self, cron_expression, start_time=None):
    #     if start_time is None:
    #         start_time = datetime.now()
    #
    #     cron_iter = croniter(cron_expression, start_time)
    #     next_run_time = cron_iter.get_next(datetime)
    #     return next_run_time
    def perform_number_crunching(self, job_id, job_details):
        try:
            numbers = list(map(int, job_details.split(',')))
            result = sum(numbers)
            logging.info(f"Successfully executed the job {job_id} with results: {result}")
            print(f"Job ID {job_id}: Sum of numbers {numbers} is {result}")
        except Exception as e:
            print(f"Failed to perform number crunching for job ID {job_id}: {e}")

    def update_next_run(self, job_id):
        # Retrieve job details
        job = self.get_job(job_id)
        if not job:
            logging.error(f"Job {job_id} not found.")
            return

        name, interval, job_details = job[1], job[2], job[3]  # Adjust indices as per your schema

        # Calculate the next run time based on the interval
        next_run_time = self.get_next_run_time(interval)

        # Update the job in the database
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(update_next_run, (next_run_time, job_id))  # Update query as needed
                conn.commit()
        finally:
            conn.close()

        # Re-schedule the job
        self.scheduler.remove_job(str(job_id))
        cron_parts = interval.split(' ')
        if len(cron_parts) == 5:  # Cron-like format
            trigger = CronTrigger(
                minute=cron_parts[0],
                hour=cron_parts[1],
                day=cron_parts[2],
                month=cron_parts[3],
                day_of_week=cron_parts[4]
            )
        else:  # Default to interval trigger in minutes
            trigger = CronTrigger(minute='*/' + interval)

        self.scheduler.add_job(
            self.execute_job,
            trigger,
            args=[job_id, job_details],
            id=str(job_id)
        )
        logging.info(f"Job {job_id} updated with next run time: {next_run_time}")

    def get_next_run_time(self, cron_expression, start_time=None):
        if start_time is None:
            start_time = datetime.now()

        cron_iter = croniter(cron_expression, start_time)
        next_run_time = cron_iter.get_next(datetime)
        return next_run_time