from . import app, scheduler


scheduler.start()
app.run()
