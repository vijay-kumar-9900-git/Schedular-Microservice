# Job Scheduler Microservice

## Overview

This project implements a job scheduling microservice using Flask, APScheduler, and PostgreSQL. It provides endpoints to manage scheduled jobs, including creating, updating, retrieving, and executing jobs based on cron-like schedules.

## Project Structure

- **Controller:** Handles API requests and routes them to the appropriate service methods.
- **Services:** Contains business logic for job scheduling, execution, and database interactions.
- **Database:** PostgreSQL is used for storing job details and scheduling information.
- **`Service.py`:** Initializes the Flask application and sets up the background scheduler ansd It Will Create Table in Database If It Not Exists.
- **`queries.py`:** Contains SQL queries used for interacting with the PostgreSQL database.
--Note: If you wish to use a different database (e.g., MySQL, SQLite), modify the db_connection.py file to configure the connection for the desired database and update the SQL queries in queries.py accordingly.

## Requirements

- Python 3.9 or later
- PostgreSQL
- Flask
- APScheduler
- psycopg2
- croniter

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository
   
2.pip install -r requirements.txt

Running the Application

1.Start the Flask Application:
python Service.py
The application In Default will run on http://127.0.0.1:5000.

2. Access the API Endpoints:

Create Job:

Endpoint: /jobs
Method: POST
Payload:
{
  "name": "Job Name",
  "interval": "0 1 * * 1",
  "job_details": "details"
}

Get All Jobs:

Endpoint: /jobs
Method: GET


Get Job by ID:

Endpoint: /get_job_id
Method: GET

API Response Status Logging
API response statuses are logged to scheduler.log.

Job Execution and Updates

One-Time Jobs: When a one-time job is executed, the last_run time is updated in the database. The next_run time is not applicable for one-time jobs and thus remains unchanged.
Recurring Jobs: For recurring jobs, after execution, both the last_run and next_run times are updated in the database. The next_run time is calculated based on the job's interval.
Example: If a job is scheduled to run every Monday at 1:00 AM (0 1 * * 1), it will execute weekly at that time. After execution, the next_run time will be updated to the next Monday at 1:00 AM and also job will automatically update (handled in code)
