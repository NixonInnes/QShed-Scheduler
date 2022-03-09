import json
from flask import request, jsonify

from qshed.client.models import Request, Schedule

from ... import scheduler
from ...request import call_request
from . import main_bp


@main_bp.route("/add", methods=["POST"])
def schedule_request():
    schedule = Schedule.parse_raw(request.data)
    scheduler.add_job(
        call_request, 
        "interval", 
        seconds=schedule.interval, 
        args=[schedule.request]
    )
    return jsonify({"response": "ok"})


@main_bp.route("/list", methods=["GET"])
def get_jobs():
    jobs = [
        Schedule(
            request=Request.parse_obj(job.args[0]),
            id=job.id,
            name=job.name,
            interval=job.trigger.interval.seconds,
            next_run=job.next_run_time.timestamp(),
        ) for job in scheduler.get_jobs()
    ]
    return jsonify([sched.dict() for sched in jobs])
