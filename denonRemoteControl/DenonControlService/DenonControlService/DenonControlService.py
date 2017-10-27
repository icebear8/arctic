
import time
import logging
import sys
from RemoteConnection import RemoteConnection
from RestService import RestService

remote = None
restService = None

def _startServices():
    global remote
    global restService

    logging.debug("Create remote connection")

    remote = RemoteConnection()

    logging.debug("Create REST service")
    restService = RestService()
    RestService.remoteConnection = remote
    restService.start()

def _runAsService():
    logging.info("Run as service")
    while True:
        time.sleep(10)

def _runAsConsole():
    logging.info("Run as console application")

    time.sleep(1)
    print("Press any key to exit...")
    input()
    _stopServices()

def _stopServices():
    logging.info("Stopping services")
    remote.disconnect()
    restService.stop()

def _initializeLogging():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
    logging.Formatter.converter = time.gmtime

if __name__ == '__main__':
    isService=False
    _initializeLogging()
    logging.info("Main started")

    for arg in sys.argv[1:]:
        if arg.upper() == "SERVICE":
            isService=True

    _startServices()

    if isService is True:
        _runAsService()
    else:
        _runAsConsole()

