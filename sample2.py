import ambient
import os
import sys
import time
import datetime
import grove_2smpb_02e

AMBIENT_CHANNEL_ID = int(os.environ['AMBIENT_CHANNEL_ID'])
AMBIENT_WRITE_KEY = os.environ['AMBIENT_WRITE_KEY']
CHECK_SPAN = int(os.environ.get('CHECK_SPAN', '30'))

sensor = grove_2smpb_02e.Grove2smpd02e()


am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY)

latest_update = datetime.datetime.now()
while True:
    press, temp = sensor.readData()
    if press is not None:

        if press.tick_last_update > latest_update:
            am.send({
                'created': data.tick_last_update.strftime('%Y-%m-%d %H:%M:%S'),
                'd1': press,
                }
            )

        latest_update = data.tick_last_update

    time.sleep(CHECK_SPAN)
