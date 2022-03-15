from fastapi import APIRouter

from qshed.client.models.data import Request, Schedule
from qshed.client.models.response import ScheduleResponse, SchedulesResponse, StrResponse

from .. import scheduler
from ..request import call_request

def get_job_as_schedule(job_id):
    try:
        job = scheduler.get_job(schedule_id)
        schedule = Schedule(
            request=Request.parse_obj(job.args[0]),
            id=job.id,
            name=job.name,
            interval=job.trigger.interval.seconds,
            next_run=job.next_run_time.timestamp(),
        )
        return Schedule
    except Exception as e:
        return None

router = APIRouter()

@router.get("/get/{job_id}", response_model=ScheduleResponse)
def get_schedule(job_id:str):
    schedule = get_job_as_schedule(job_id)
    if schedule:
        return ScheduleResponse(content=schedule)
    else:
        return ScheduleResponse(ok=False, message=f"Failed to get schedule {job_id}")


@router.post("/add", response_model=StrResponse)
def add_schedule(schedule:Schedule):
    try:
        job = scheduler.add_job(
            call_request, 
            "interval", 
            seconds=schedule.interval, 
            args=[schedule.request]
        )
        return StrResponse(message="Schedule created", content=job.id)
    except Exception as e:
        return StrResponse(ok=False, message="Failed to create schedule", content="")


@router.get("/list", response_model=SchedulesResponse)
def get_schedules():
    try:
        schedules = [
            Schedule(
                request=Request.parse_obj(job.args[0]),
                id=job.id,
                name=job.name,
                interval=job.trigger.interval.seconds,
                next_run=job.next_run_time.timestamp(),
            ) for job in scheduler.get_jobs()
        ]
        return SchedulesResponse(content=schedules)
    except Exception as e:
        return SchedulesResponse(ok=False, message="Failed to retrieve schedules")
