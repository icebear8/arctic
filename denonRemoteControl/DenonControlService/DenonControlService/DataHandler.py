
import logging
import socket
import threading
from enum import Enum

from abc import ABC, abstractmethod
from RemoteConnection import IResponseHandler

_dataCache = None

def getData():
    global _dataCache
    if _dataCache == None:
        _dataCache = DeviceData()
    return _dataCache

class PowerState(Enum):
    ON = 0
    OFF = 1
    UNKNOWN = 2

class DeviceData:
    def __init__(self):
        self.volume = 0.0
        self.power = PowerState.UNKNOWN

class VolumeHandler(IResponseHandler):
    def __init__(self):
        super(VolumeHandler, self).__init__("MV")
    def handleResponse(self, line):
        pass
