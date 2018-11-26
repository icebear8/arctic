
import logging
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
  return "Service started"

@app.route('/service/stop', methods=['PUT'])
def stopService():
  logging.info("Service stopped")
  return "Service stopped"
    
@app.route('/')
def hello_world():
    logging.info("Root url called")
    return 'Hello, World!'

class RestService(threading.Thread):
  isServiceRunning = True

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
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
  logging.info("Main started")
  restService = RestService()
  
  if len(sys.argv) >= 2:
    try:
      restService._port = int(sys.argv[1])
    except ValueError:
      pass    # Nothing to do
  
  restService.start()
  
  logging.info("Wait loop")
  while RestService.isServiceRunning:
    time.sleep(10)
    
  logging.info("Exit main")
