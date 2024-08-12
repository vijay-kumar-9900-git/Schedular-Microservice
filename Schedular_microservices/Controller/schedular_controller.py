from flask import Blueprint, request, jsonify
from Services import schedular_services
job_bp = Blueprint('job_bp', __name__)
job_service = schedular_services.JobService()
@job_bp.route('/create_jobs', methods=['POST'])
def create_job():
    result = job_service.create_job(request.get_json())
    return jsonify(result),201

@job_bp.route('/get_jobs', methods=['GET'])
def get_jobs():
    jobs = job_service.get_jobs()
    return jsonify(jobs),200

@job_bp.route('/get_job_id', methods=['GET'])
def get_job():
    job = job_service.get_job(request.json)
    if job:
        return jsonify(job),200
    else:
        return jsonify({"error": "Job not found"}),404
