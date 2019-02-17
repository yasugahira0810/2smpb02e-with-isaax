from logging import getLogger
logger = getLogger(__name__)

from omron_envsensor import OmronEnvSensor
from omron_envsensor.util import getHostname
import uuid
import random
import sys
from threading import Thread
import time


ADDRESSESS_KEEPALIVE = 10


class EnvStatus(Thread):
    filters = {}
    active_devices = {}

    def __init__(self, hostname=None, bt=0, daemon=True, *args, **kwargs):
        if hostname is None:
            hostname = getHostname()

        self.omron = OmronEnvSensor(hostname, bt)
        self.omron.on_message = self.callback

        super(EnvStatus, self).__init__(daemon=daemon, *args, **kwargs)

    def run(self):
        logger.debug('omron start')
        self.omron.init()
        try:
            self.omron.loop()
        except Exception as e:
            logger.exception(e)

    def setRequest(self, address):
        uId = str(uuid.uuid4())
        self.filters[uId] = [address, None]
        logger.debug('filters is %s', self.filters)
        return uId

    def rmRequest(self, uId):
        try:
            del self.filters[uId]
        except Exception as e:
            logger.exception(e)

        logger.debug('filters is %s', self.filters)

    def getLatestData(self, uId):
        return self.filters[uId][1]

    def callback(self, beacon):
        address = beacon.bt_address.replace(':', '').upper()
        logger.debug('get beacon %s', address)
        self.addDevice(address)
        for k, i in self.filters.items():
            if i[0] == address:
                logger.debug('hit %s', address)
                i[1] = beacon

    def addDevice(self, address):
        now = time.time()
        self.active_devices[address] = now

        if 1 > random.choice([i for i in range(0, 10)]):
            self.refreshDevices()


    def refreshDevices(self):
        now = time.time()
        removes = []
        for i in self.active_devices.keys():
            if now > self.active_devices[i] + ADDRESSESS_KEEPALIVE:
                removes.append(i)

        for i in removes:
            del self.active_devices[i]
        logger.debug('current devices is %s', self.active_devices)

    def getCurrentDevices(self):
        self.refreshDevices()
        return self.active_devices.keys()
