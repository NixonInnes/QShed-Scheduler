import uvicorn
from . import scheduler


scheduler.start()
uvicorn.run("scheduler:app", host="0.0.0.0", port=4500)
