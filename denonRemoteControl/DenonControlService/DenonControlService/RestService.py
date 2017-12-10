
import logging
import threading
import time
import http.client

from flask import Flask
from flask import render_template
from flask import request

from RemoteConnection import RemoteConnection

versionId = '0.1.1:20161130'

app = Flask(__name__)

def _runProcess():
  app.run(host='0.0.0.0')

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/maintenance")
def maintenance():
  return render_template('maintenance.html')

@app.route("/demo")
def demo():
  return render_template('demo.html')

@app.route('/version')
def getVersion():
  return versionId

@app.route('/hello', methods=['GET'])
def getHello():
  return "Hello flask"

@app.route('/command', methods=['GET', 'POST', 'PUT'])
def getCmd():
  command = request.args.get('cmd')
  logging.info("Wildcard command request: %s", command)

  if not command.endswith('\r'):
    command += '\r'
  RestService.remoteConnection.send(command)
  return command

@app.route('/volume', methods=['GET'])
def getVolume():
  logging.info("Volume get request")
  RestService.remoteConnection.send("MV?\r")
  logging.info("Current volume: " + str(RestService.remoteConnection.data.volume))
  return str(RestService.remoteConnection.data.volume)

@app.route('/power', methods=['GET'])
def getPower():
  logging.info("Power get request")
  RestService.remoteConnection.send("PW?\r")
  return "Power"

@app.route('/power/<cmd>', methods=['PUT'])
def setPower(cmd):
  message = ""
  logging.info("Power set request:" + str(cmd))
  message = "PW" + str(cmd).upper() + "\r"
  RestService.remoteConnection.send(message)
  return "Power"

@app.route('/start', methods=['PUT'])
def start():
  logging.info("Start request")
  RestService.remoteConnection.send("PWON\r")
  time.sleep(5)
  RestService.remoteConnection.send("MV28\r")
  RestService.remoteConnection.send("SIFAVORITES\r")
  time.sleep(2)
  RestService.remoteConnection.send("NS94\r") # enter
  return "Start";

@app.route('/startVolume/<volume>', methods=['PUT'])
def startVolume(volume):
  volumeCommand = "MV" + str(volume).upper() + "\r";
  logging.info("Start volume request")
  RestService.remoteConnection.send("PWON\r")
  time.sleep(5)
  RestService.remoteConnection.send(volumeCommand)
  RestService.remoteConnection.send("SIFAVORITES\r")
  time.sleep(2)
  RestService.remoteConnection.send("NS94\r") # enter
  return "Start";

@app.route('/next', methods=['PUT'])
def next():
  logging.info("Next request")
  RestService.remoteConnection.send("SIFAVORITES\r")
  time.sleep(2)
  RestService.remoteConnection.send("NS91\r") # next
  time.sleep(1)
  RestService.remoteConnection.send("NS94\r") # enter
  return "Next";

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

@app.route('/connection', methods=['GET'])
def getConnection():
  return RestService.remoteConnection.isConnected()

@app.route('/connection/<command>', methods=['PUT'])
def connection(command):
  logging.info("Connection command received: %s", command)
  connectionCommand = str(command).upper()
	
  if connectionCommand == 'DISCONNECT':
    RestService.remoteConnection.disconnect()
    
  if connectionCommand == 'CONNECT':
    RestService.remoteConnection.connect()

  return "Connection command executed";

class RestService(threading.Thread):
  isShutdownAllowed = True
  remoteConnection = None

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
