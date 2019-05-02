
import logging
import threading
import time
import DataCache as cache

logger = logging.getLogger(__name__)

_id = 'line'
_prefix = 'NSE'
_timeLastCreated = 0.0
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
  '8' : cache.CachedValue(_id + "8")
}

def getId():
  return _id

def cmdPrefix():
  return _prefix

def createRequest(request='get'):
  global _timeLastCreated
  timeDiff = time.time() - _timeLastCreated
  _timeLastCreated = time.time()

  logger.debug('Last request, diff: %s, lastTime: %s', str(timeDiff), str(_timeLastCreated))
  if (timeDiff) < _REQUEST_INTERVAL_SEC:
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
      global _timeLastCreated
      _timeLastCreated = time.time()
      reply = _removeNonPrintableChars(reply)
      key = getId() + reply[3]
      text = '' + reply[4:].strip()
      _cachedValues[reply[3]].update(text)
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

def workaroundDenonProtocol(lines):
  idx = 0
  for line in lines:
    if line.startswith("NSE") or line.startswith("NSA"):
      if ((len(line) == 4) and (idx < len(lines)) and (not (lines[idx + 1].startswith("NSE") or (lines[idx + 1].startswith("NSE"))))):
        logger.debug("Denon workaround: %s", line[:4])
        lines[idx] += "\r" + lines[idx + 1]
    ++idx
  return lines
