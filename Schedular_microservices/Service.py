from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from Controller import schedular_controller
from db_connection import setup_database
app = Flask(__name__)


bg_scheduler = BackgroundScheduler(daemon=True)
bg_scheduler.start()


app.register_blueprint(schedular_controller.job_bp)


if __name__ == '__main__':
    setup_database()
    app.run(host='127.0.0.1', port=5000, debug=True)
