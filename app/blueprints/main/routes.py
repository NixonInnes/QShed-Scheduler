import json
from flask import request, jsonify

from qshed.client.models import Request, Schedule

from ... import scheduler
from ...request import call_request
from . import main_bp


@main_bp.route("/get/<job_id:str>", methods=["GET"])
def get_job(job_id):
    ok = True
    response = None

    try:
        job = scheduler.get_job(job_id)
        schedule = Schedule(
            request=Request.parse_obj(job.args[0]),
            id=job.id,
            name=job.name,
            interval=job.trigger.interval.seconds,
            next_run=job.next_run_time.timestamp(),
        )
        response = schedule.dict() 
    except Exception as e:
        ok = False
        response = {"error": str(e)}

    return jsonify((ok, response))



@main_bp.route("/add", methods=["POST"])
def schedule_request():
    ok = True
    response = None
    
    try:
        schedule = Schedule.parse_raw(request.data)
    except Exception as e:
        schedule = None
        ok = False
        response = {"error": str(e)}

    if schedule:
        try:
            job = scheduler.add_job(
                call_request, 
                "interval", 
                seconds=schedule.interval, 
                args=[schedule.request]
            )
            response = {"id": job.id}
        except Exception as e:
            ok = False
            response = {"error": str(e)}

    return jsonify((ok, response))


@main_bp.route("/list", methods=["GET"])
def get_jobs():
    ok = True
    response = None

    try:
        jobs = [
            Schedule(
                request=Request.parse_obj(job.args[0]),
                id=job.id,
                name=job.name,
                interval=job.trigger.interval.seconds,
                next_run=job.next_run_time.timestamp(),
            ) for job in scheduler.get_jobs()
        ]
        response = [sched.dict() for sched in jobs]
    except Exception as e:
        ok = False
        response = {"error": str(e)}

    return jsonify((ok, response))
