import time
from crontab import CronTab

def update_water_cycle(output_pin, start_time, duration, water_id):
    cron = CronTab(user=True)
    job = cron.new(command='python3 /home/ajh149/repos/hydro_flask/water_pump.py {} {}'.format(output_pin, duration))
    job.comment = water_id
    job.day.every(1)
    job.hour.on(start_time)
    cron.write()

update_water_cycle(8, 6, 5, "test")