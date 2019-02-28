from __future__ import print_function

import ambient
import os
import sys
import time
import datetime
import grove_2smpb_02e

from flask import Flask
from flask import render_template
from flask import jsonify

AMBIENT_CHANNEL_ID = int(os.environ['AMBIENT_CHANNEL_ID'])
AMBIENT_WRITE_KEY = os.environ['AMBIENT_WRITE_KEY']
AMBIENT_READ_KEY = os.environ['AMBIENT_READ_KEY']
CHECK_SPAN = int(os.environ.get('CHECK_SPAN', '30'))

sensor = grove_2smpb_02e.Grove2smpd02e()
app = Flask(__name__)

am = ambient.Ambient(AMBIENT_CHANNEL_ID, AMBIENT_WRITE_KEY, AMBIENT_READ_KEY)

latest_update = datetime.datetime.now()
while True:
    press, temp = sensor.readData()
    if press is not None and temp is not None:
        am.send(
            {
                'd1': press,
                'd2': temp,
            }
        )
        d = am.read(n=1)
        print(d)
        
    time.sleep(CHECK_SPAN)
