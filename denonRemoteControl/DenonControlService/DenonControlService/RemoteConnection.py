
import logging
import socket
import threading

defaultHost = '192.168.0.50'
defaultIp = '192.168.0.50'
defaultPort = 23
bufferSize = 1024

class DeviceData:
    def __init__(self):
        self.volume = 0

class RemoteConnection:
    def __init__(self):
        self._ip = defaultIp
        self._port = defaultPort
        self._socket = socket.socket()
        self._isConnected = False
        self._listenerThread = None
        self.data = DeviceData()

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        if self._isConnected is True:
            self.disconnect()
        self._ip = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if self._isConnected is True:
            self.disconnect()
        self._port = port

    @property
    def isConnected(self):
        return self._isConnected

    def connect(self):
        if self._isConnected is True:
            self.disconnect()
        
        try:
            self._socket = socket.socket()
            self._ip = socket.gethostbyname(defaultHost)
        except socket.gaierror as ex:
            logging.error("Unable to get IP from host: " + defaultHost)
            logging.exception(ex)
            return

        logging.info("Connect to: " + self._ip)
        
        self._socket.connect((self._ip, self._port))
        self._listenerThread = ListenerThread(self._socket, self.data)
        self._isConnected = True
        self._listenerThread.start()

    def disconnect(self):
        logging.info("Disconnect method called")
        
        if self._isConnected is True:
            logging.info("Disconnect")
            self._listenerThread.abort()
            self._listenerThread.join()
            self._socket.close()

        logging.info("Disconnected")
        self._isConnected = False

    def send(self, message):
        if not self._isConnected:
            self.connect()
        logging.debug("Send: %s", message.strip())

        if self._isConnected is True:
            self._socket.send(message.encode('ASCII'))
        else:
            logging.error("Unable to send command: %s", message.strip())
        
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
        logging.info('Start listener thread')
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
                        for line in lines:
                            if len(line) > 5 and line.startswith('NSE') and (not line.startswith('NSE0') or line.startswith('NSE7') or line.startswith('NSE8')):
                                line = line.replace(line[4], ' ')
                            if line.startswith('MV'):
                                if line[2:].isdecimal():
                                    logging.info("Volume received: " + line[2:])
                                    self.deviceData.volume = line[2:]
                            logging.info("Received: " + line)
                    except UnicodeDecodeError:
                        logging.info("Decode error: " + str(data))
                        pass    # Nothing to do


            self._lock.acquire()
            isRunning = self._isListening
            self._lock.release()

            logging.debug("loop: " + str(i) + ", running: " + str(isRunning))

        logging.info('End listener thread')
