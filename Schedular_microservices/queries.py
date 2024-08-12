create_job_query = '''
    INSERT INTO jobs (name, interval, job_details) 
    VALUES (%s, %s, %s) RETURNING id;
'''

get_jobs_query = 'SELECT * FROM jobs;'

get_job_query = 'SELECT * FROM jobs WHERE id = %s;'

update_last_run = """
    UPDATE jobs
    SET  last_run = %s
    WHERE id = %s
"""

update_next_run = """
UPDATE jobs
SET
    next_run = %s
WHERE id = %s;
"""
