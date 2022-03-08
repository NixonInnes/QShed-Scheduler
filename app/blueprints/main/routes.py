import json
from flask import request, jsonify

from ... import scheduler
from ...request import Request
from . import main_bp


@main_bp.route("/sched", methods=["POST"])
def schedule_request():
    data = request.get_json(force=True)
    data = {k:v for k,v in json.loads(data).items() if k in ["url","method","headers","data","params"]}
    scheduler.add_job(Request.scheduler_call, "interval", seconds=10, kwargs=data)
    return jsonify({"response": "ok"})


@main_bp.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = [
        {
            "id": job.id,
            "name": job.name,
            "kwargs": job.kwargs,
            #"next_run_time": job.next_run_time
        } for job in scheduler.get_jobs()
    ]
    return json.dumps(jobs)
