
import logging
import threading
import time

from flask import Flask

app = Flask(__name__)

def _runProcess():
  app.run(host='0.0.0.0')
  
@app.route('/shutdown', methods=['PUT'])
def shutdown():
  logging.info("Shutdown post")

  if RestService.isShutdownAllowed is True:
    logging.info("Server shutting down")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Server shutting down"
  else:
    return "Shutdown not allowed"

@app.route('/service/start', methods=['PUT'])
def startService():
  logging.info("Service started")
  return "Service started"

@app.route('/service/stop', methods=['PUT'])
def stopService():
  logging.info("Service stopped")
  return "Service stopped"
    
class RestService(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def run(self):
    logging.info("Rest service started")
    _runProcess()

  def stop(self):
    logging.info("Stopping rest service")
    restClient = http.client.HTTPConnection("localhost", 5000)
    restClient.request("PUT", "/shutdown", None)
    logging.info("Rest service stopped")

if __name__ == '__main__':
  logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.INFO)
  logging.info("Main started")
  restService = RestService()
  restService.start()

  print("Press any key to exit...")
  input()
  restService.stop()