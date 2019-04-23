
import logging
import socket
import threading

import commands.Volume as cmdVolume
import commands.Power as cmdPower
import commands.Nse as cmdNse

logger = logging.getLogger(__name__)

defaultIp = '192.168.0.0'
defaultHost = defaultIp
defaultPort = 23
bufferSize = 1024
defaultInactivityTimeoutSec = 300.0

class DeviceData:
  def __init__(self):
    self.volume = 0

class RemoteConnection:
  def __init__(self, host, port=defaultPort):
    self._ip = defaultIp
    if host:
      self._host=host
    else:
      self._host=defaultHost

    self._port = port
    self._inactivityTimeoutSec = defaultInactivityTimeoutSec

    self._socket = socket.socket()
    self._isConnected = False
    self._listenerThread = None
    self._disconnectTimer = None
    self.data = DeviceData()

  @property
  def port(self):
    return self._port

  @port.setter
  def port(self, port):
    if self._isConnected is True:
      self.disconnect()
    self._port = port

  @property
  def inactivityTimeoutSec(self):
    return self._inactivityTimeoutSec

  @inactivityTimeoutSec.setter
  def inactivityTimeoutSec(self, timeoutSec):
    logger.debug("Set inactivity timeout (sec): " + timeoutSec)
    try:
        self._inactivityTimeoutSec = int(timeoutSec)
    except ValueError:
        logger.debug("Inactivity cannot be converted to a number: " + timeoutSec)
        return
    self._restartConnectionTimeout()

  @property
  def isConnected(self):
    return self._isConnected

  def connect(self):
    if self._isConnected is True:
      self.disconnect()

    try:
      self._socket = socket.socket()
      self._ip = socket.gethostbyname(self._host)
    except socket.gaierror as ex:
      logger.error("Unable to get IP from host: " + self._host)
      logger.exception(ex)
      return

    logger.debug("Connect to: " + self._ip)

    self._socket.connect((self._ip, self._port))
    self._listenerThread = ListenerThread(self._socket, self.data)
    self._isConnected = True
    self._listenerThread.start()

  def disconnect(self):
    logger.debug("Disconnect method called")

    if self._isConnected is True:
      logger.debug("Disconnect")
      self._listenerThread.abort()
      self._listenerThread.join()
      self._socket.close()

    logger.debug("Disconnected")
    self._isConnected = False

  def send(self, message):
    self._restartConnectionTimeout()
    if not self._isConnected:
      self.connect()
    logger.debug("Send: %s", message.strip())

    if self._isConnected is True:
      self._socket.send(message.encode('ASCII'))
    else:
      logger.error("Unable to send command: %s", message.strip())
      self.disconnect()

  def _restartConnectionTimeout(self):
    if self._disconnectTimer is not None:
      self._disconnectTimer.cancel()

    self._disconnectTimer = threading.Timer(self._inactivityTimeoutSec, self.disconnect)
    if self._isConnected is True:
      self._disconnectTimer.start()

class ListenerThread(threading.Thread):
  def __init__(self, socket, data):
    threading.Thread.__init__(self)
    self._socket = socket
    self._isListening = True
    self._lock = threading.Lock()
    self.deviceData = data

  def abort(self):
    self._lock.acquire()
    self._isListening = False
    self._lock.release()

  def run(self):
    isRunning = True
    logger.debug('Start listener thread')
    i = 0
    data = []

    self._socket.settimeout(1)
    while isRunning is True:
      i += 1
      try:
        data = self._socket.recv(bufferSize)
      except socket.timeout:
        pass    # Nothing to do
      else:
        if data:
          try:
            lines = data.decode('UTF-8').split('\r')
            self._processLines(lines)
          except UnicodeDecodeError:
            logger.info("Unicode decode error")
            pass    # Nothing to do

      self._lock.acquire()
      isRunning = self._isListening
      self._lock.release()

    logger.debug('End listener thread')

  def _processLines(self, lines):
    for line in lines:
      line = _removeNonPrintableChars(line)
      logger.debug("Received line: " + line)

      reply = cmdVolume.processReply(line)
      if reply is not None:
        logger.debug("Volume decoded: " + reply)
        self.deviceData.volume = reply

      reply = cmdPower.processReply(line)
      if reply is not None:
        logger.debug("Power decoded: " + reply)

      reply = cmdNse.processReply(line)
      if reply is not None:
        logger.debug("Display decoded: %s", reply)

def _removeNonPrintableChars(line):
  if (len(line) >= 5) and (line.startswith('NSA') or line.startswith('NSE')):
    if line[3] in ('1', '2', '3', '4', '5', '6'):
      line = line.replace(line[4], '')
  return line
