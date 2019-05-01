
import logging
import time
import DataCache as cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_id = 'line'
_prefix = 'NSE'
_timeLastReceiveSec = 0.0
_REQUEST_INTERVAL_SEC = 2.0

_cachedValues = {
  '0' : cache.CachedValue(_id + "0"),
  '1' : cache.CachedValue(_id + "1"),
  '2' : cache.CachedValue(_id + "2"),
  '3' : cache.CachedValue(_id + "3"),
  '4' : cache.CachedValue(_id + "4"),
  '5' : cache.CachedValue(_id + "5"),
  '6' : cache.CachedValue(_id + "6"),
  '7' : cache.CachedValue(_id + "7"),
  '8' : cache.CachedValue(_id + "8"),
  'artist' : cache.CachedValue(_id + "Artist"),
  'title' : cache.CachedValue(_id + "Title"),
  'album' : cache.CachedValue(_id + "Album"),
}

def getId():
  return _id

def cmdPrefix():
  return _prefix

def getValue(key=_id):
  if key in _cachedValues.keys():
    return _cachedValues[key].getValue()
  elif key in (_id):
    return getValues()
  logger.debug("Invalid key: " + key)
  return ''

def waitValue(key=_id, timeout=None):
  if key in _cachedValues:
    return _cachedValues[key].waitValue(timeout)
  elif key in (_id):
    return waitValues(timeout)
  logger.debug("Invalid key: " + key)
  return ''

def getValues():
  lines = ''
  for key in _cachedValues:
    if len(key) <= 2:
      lines += _cachedValues[key].getValue() + '\n'
  return lines

def waitValues(timeout=None):
  lines = ''
  for key in _cachedValues:
    if len(key) <= 2:
      lines += _cachedValues[key].waitValue(timeout) + '\n'
  return lines

def createRequest(request):
  global _timeLastReceiveSec
  logger.debug('Last request, diff: %s, lastTime: %s', str(time.time() - _timeLastReceiveSec), str(_timeLastReceiveSec))
  if (time.time() - _timeLastReceiveSec) < _REQUEST_INTERVAL_SEC:
    logger.debug('Ignore too frequent requests')
    return ''
  for key in _cachedValues:
    _cachedValues[key].invalidate()
  request = request.upper()
  if request in ('GET'):
    return cmdPrefix() + '\r'
  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  if reply.startswith(cmdPrefix()):
    return reply[3].isdecimal()
  return False

def processReply(reply):
  if isProcessible(reply) is True:
      global _timeLastReceiveSec
      _timeLastReceiveSec = time.time()
      reply = _removeNonPrintableChars(reply)
      key = getId() + reply[3]
      text = '' + reply[4:].strip()
      _cachedValues[reply[3]].update(text)
      _handleSpecialInfo(reply[3], text)
      logger.debug('Processed %s: %s', reply[3], text)
      return { key : text }
  return None

def _logCursorInfo(reply):
  if len(reply) < 5:
    return
  if reply[3] not in ('1', '2', '3', '4', '5', '6'):
    return
  info = ord(reply[4])

  text = "Line info " + reply[3] + ":"
  if info & 0x01:
    text += " 'playable'"
  if info & 0x02:
    text += " 'directory'"
  if info & 0x08:
    text += " 'cursor'"
  if info & 0x40:
    text += " 'picture'"
  if len(text) > 12:
    logger.debug(text)
  return

def _removeNonPrintableChars(reply):
  if (len(reply) >= 5):
    if reply[3] in ('1', '2', '3', '4', '5', '6'):
      reply = reply.replace(reply[4], '')
  return reply

def _handleSpecialInfo(id, text):
  if (_cachedValues['0'].getValue().startswith("Now Playing")):
    if id is '1':
      logger.debug("Title: %s", text)
      _cachedValues['title'].update(text)
    elif id is '2':
      logger.debug("Artist: %s", text)
      _cachedValues['artist'].update(text)
    elif id is '4':
      logger.debug("Album: %s", text)
      _cachedValues['album'].update(text)

def workaroundDenonProtocol(lines):
  idx = 0
  for line in lines:
    if line.startswith("NSE") or line.startswith("NSA"):
      if ((len(line) == 4) and (idx < len(lines)) and (not (lines[idx + 1].startswith("NSE") or (lines[idx + 1].startswith("NSE"))))):
        logger.debug("Denon workaround: %s", line[:4])
        lines[idx] += "\r" + lines[idx + 1]
    ++idx
  return lines
