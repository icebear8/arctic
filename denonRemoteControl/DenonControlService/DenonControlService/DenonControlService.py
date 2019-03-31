
import getopt
import time
import logging
import sys
from RemoteConnection import RemoteConnection
from RestService import RestService

remote = None
restService = None

def _startServices(host):
  global remote
  global restService

  logging.debug("Create remote connection")

  remote = RemoteConnection(host)

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

def _printUsage():
  print('DenonControlService.py [-s --host=]')
  print('-s: Start as service')
  print('--host=: Host name or IP to connect')
  
def main(argv):
  isService=False
  host=""
  
  _initializeLogging()
  logging.info("Main started")
  
  try:
    opts, args = getopt.getopt(argv, "hs", ["help", "host="])
  except getopt.GetoptError as err:
    print(err)  # will print something like "option -a not recognized"
    _printUsage()
    sys.exit(2)
      
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      _printUsage()
      sys.exit()
    elif opt in ('-s'):
      isService=True
    elif opt in ('--host'):
      host=arg

  _startServices(host)

  if isService is True:
    _runAsService()
  else:
    _runAsConsole()
  
if __name__ == '__main__':
  main(sys.argv[1:])


