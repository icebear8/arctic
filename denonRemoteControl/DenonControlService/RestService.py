
import logging
import threading
import time
import http.client

import DataCache as cache

import commands.Nse as cmdLines
import commands.Power as cmdPower
import commands.Source as cmdSource
import commands.Volume as cmdVolume
import evaluators.NowPlaying as evlPlaying

from flask import Flask
from flask import render_template
from flask import request

from RemoteConnection import RemoteConnection

app = Flask(__name__)
logger = logging.getLogger(__name__)

defaultRequestTimeout = 0.4    # 400ms

def _runProcess():
  app.run(host='0.0.0.0')

def _handleRequest(command, request='get'):
  logger.debug(command.getId() + " request: " + request)
  cmdRequest = command.createRequest(request)

  if cmdRequest is not None:
    RestService.remoteConnection.send(cmdRequest)
    return cache.waitValue(key=command.getId(), timeout=defaultRequestTimeout)

  logger.debug(command.getId() + "unknown request: " + request)
  return "Invalid request"


@app.route("/")
def index():
  return render_template('index.html')

@app.route('/hello', methods=['GET'])
def getHello():
  return "Hello Denon Service"

@app.route('/command', methods=['GET', 'POST', 'PUT'])
def getCmd():
  command = request.args.get('cmd')
  logger.debug("Wildcard command request: %s", command)

  if not command.endswith('\r'):
    command += '\r'
  RestService.remoteConnection.send(command)
  return command

@app.route('/volume', methods=['GET'])
def getVolume():
  return _handleRequest(cmdVolume, 'get')

@app.route('/volume/<request>', methods=['PUT'])
def setVolume(request):
  return _handleRequest(cmdVolume, request)

@app.route('/power', methods=['GET'])
def getPower():
  return _handleRequest(cmdPower, 'get')

@app.route('/power/<request>', methods=['PUT'])
def setPower(request):
  return _handleRequest(cmdPower, request)

@app.route('/display/lines')
def lines():
    command = cmdLines
    logger.debug(command.getId() + " request: get")
    cmdRequest = command.createRequest('get')

    if cmdRequest is not None:
      RestService.remoteConnection.send(cmdRequest)
      return cache.waitQuery(query=command.getId(), timeout=defaultRequestTimeout)

    logger.debug(command.getId() + "unknown request: " + request)
    return "Invalid request"

@app.route('/display/line/<request>')
def line(request):
  command = cmdLines
  logger.debug(command.getId() + " request: " + request)
  cmdRequest = command.createRequest('get')

  if cmdRequest is not None:
    RestService.remoteConnection.send(cmdRequest)
    return cache.waitValue(key=command.getId() + request, timeout=defaultRequestTimeout)

  logger.debug(command.getId() + "unknown request: " + request)
  return "Invalid request"

@app.route('/playing/<request>')
def nowPlaying(request):
  evaluator = evlPlaying
  logger.debug(evaluator.getId() + " request: " + request)
  cmdRequest = evaluator.createRequest()

  if cmdRequest is not None:
    RestService.remoteConnection.send(cmdRequest)
    evaluator.evaluate(timeout=defaultRequestTimeout)
    return cache.getValue(key=request)

  logger.debug(evaluator.getId() + "unknown request: " + request)
  return "Invalid request"

@app.route('/source')
def getSource():
  return _handleRequest(cmdSource, 'get')

@app.route('/start', methods=['PUT'])
def start():
  logger.debug("Start request")
  RestService.remoteConnection.send("PWON\r")
  time.sleep(5)
  RestService.remoteConnection.send("SIFAVORITES\r")
  time.sleep(2)
  RestService.remoteConnection.send("NS94\r") # enter
  return "Start";

@app.route('/startVolume/<volume>', methods=['PUT'])
def startVolume(volume):
  volumeCommand = "MV" + str(volume).upper() + "\r";
  logger.debug("Start volume request")
  RestService.remoteConnection.send("PWON\r")
  time.sleep(5)
  RestService.remoteConnection.send(volumeCommand)
  RestService.remoteConnection.send("SIFAVORITES\r")
  time.sleep(3)
  RestService.remoteConnection.send("NS94\r") # enter
  return "Start";

@app.route('/next', methods=['PUT'])
def next():
  logger.info("Next request")
  RestService.remoteConnection.send("SIFAVORITES\r")
  time.sleep(3)
  RestService.remoteConnection.send("NS91\r") # next
  time.sleep(1)
  RestService.remoteConnection.send("NS94\r") # enter
  return "Next";

@app.route('/shutdown', methods=['PUT'])
def shutdown():
  logger.info("Shutdown post")

  if RestService.isShutdownAllowed is True:
    logger.info("Server shutting down")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Server shutting down"
  else:
    return "Shutdown not allowed"

@app.route('/connection', methods=['GET'])
def getConnection():
  if RestService.remoteConnection.isConnected is True:
    return "Connected"

  return "Disconnected"

@app.route('/connection/<command>', methods=['PUT'])
def connection(command):
  logger.debug("Connection command received: %s", command)
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
    logger.info("Rest service started")
    _runProcess()

  def stop(self):
    logger.info("Stopping rest service")
    restClient = http.client.HTTPConnection("localhost", 5000)
    restClient.request("PUT", "/shutdown", None)
    logger.info("Rest service stopped")
