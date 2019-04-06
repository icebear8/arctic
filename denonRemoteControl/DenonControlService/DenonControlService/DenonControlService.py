
import getopt
import time
import logging
import sys
from RemoteConnection import RemoteConnection
from RestService import RestService

remote = None
restService = None

def _runServices(targetHost, timeout):
  global remote
  global restService

  logging.debug("Create remote connection")

  remote = RemoteConnection(host=targetHost)
  
  if timeout:
    remote.inactivityTimeoutSec = timeout

  logging.debug("Create REST service")
  restService = RestService()
  RestService.remoteConnection = remote
  restService.start()

  while True:
    time.sleep(10)

def _stopServices():
  logging.info("Stopping services")
  remote.disconnect()
  restService.stop()

def _initializeLogging(loglevel):
  numeric_level = getattr(logging, loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    numeric_level = getattr(logging, INFO, None)

  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=numeric_level)
  logging.Formatter.converter = time.gmtime

def _printUsage():
  print('DenonControlService.py [--host=, --log=, --timeout=]')
  print('--host=: Host name or IP to connect')
  print('--log=: Loglevel [DEBUG, INFO, WARNING, ERROR, CRITICAL]')
  print('--timeout=: Inactivity disconnection timeout in seconds (default=300 sec)')
  
def main(argv):
  isService = False
  host = ""
  loglevel = ""
  timeout = None
  
  try:
    opts, args = getopt.getopt(argv, "h", ["help", "host=", "log=", "timeout="])
  except getopt.GetoptError as err:
    print(err)  # will print something like "option -a not recognized"
    _printUsage()
    sys.exit(2)
      
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      _printUsage()
      sys.exit()
    elif opt in ('--host'):
      host = arg
    elif opt in ('--log='):
      loglevel = arg
    elif opt in ('--timeout='):
      timeout = arg
    

  _initializeLogging(loglevel)
  logging.info("Main started")

  _runServices(host, timeout)
  
if __name__ == '__main__':
  main(sys.argv[1:])


