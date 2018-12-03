

import logging
import os
import signal
import subprocess
import sys
import threading
import time

from flask import Flask
from flask import request

app = Flask(__name__)

def _runProcess(listeningPort):
  app.run(host='0.0.0.0', port=listeningPort)
  
@app.route('/shutdown', methods=['PUT'])
def shutdown():
  logging.info("Shutdown post")
  
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
  func()
  
  RestService.isServiceRunning = False
  return "Server shutting down"

@app.route('/service/start', methods=['PUT'])
def startService():
  logging.info("Service started")
  if RestService.runningProcess is None:
    if RestService.commandToRun is not None:
      logging.info("Start service");
      RestService.runningProcess = subprocess.Popen(RestService.commandToRun, preexec_fn=os.setsid)
    else:
      logging.info("Command not valid");
      return "Service cannot be started"
  else:
    logging.info("Service already running");

  return "Service running"

@app.route('/service/stop', methods=['PUT'])
def stopService():
  logging.info("Service stopped")
  if RestService.runningProcess is not None:
    logging.info("Kill running process");
    os.killpg(os.getpgid(RestService.runningProcess.pid), signal.SIGTERM)
    RestService.runningProcess = None
  else:
    logging.info("No service running");
  
  return "Service stopped"
  
@app.route('/service', methods=['GET'])
def isServiceRunning():
  logging.info("Service stopped")
  if RestService.runningProcess is not None:
    return "Service running"

  return "Service stopped"
    
@app.route('/')
def hello_world():
    logging.info("Root url called")
    return 'Hello, World!'

class RestService(threading.Thread):
  isServiceRunning = True
  runningProcess = None
  commandToRun = []

  def __init__(self):
    threading.Thread.__init__(self)
    self._port = 58051

  def run(self):
    logging.info("Rest service started")
    _runProcess(self._port)

  def stop(self):
    logging.info("Stopping rest service")
    restClient = http.client.HTTPConnection("localhost", self._port)
    restClient.request("PUT", "/shutdown", None)
    logging.info("Rest service stopped")

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.WARNING)
  logging.info("Main started")
  restService = RestService()
  
  if len(sys.argv) >= 2:
    try:
      restService._port = int(sys.argv[1])
    except ValueError:
      pass    # Nothing to do

  if len(sys.argv) >= 3:
    for i in range(2, len(sys.argv)):
      RestService.commandToRun.append(sys.argv[i])

  logging.info("Command to run: " + " ".join(RestService.commandToRun))
  
  restService.start() # Start rest thread
  startService()  # Initially start the command to be executed
  
  logging.info("Wait loop")
  while RestService.isServiceRunning:
    time.sleep(10)
    
  logging.info("Exit main")
