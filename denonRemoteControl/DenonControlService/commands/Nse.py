
import logging
import DataCache as cache

logger = logging.getLogger(__name__)

_id = 'line'
_prefix = 'NSE'

cachedValues = {
  '0' : cache.CachedValue(_id + "0"),
  '1' : cache.CachedValue(_id + "1"),
  '2' : cache.CachedValue(_id + "2"),
  '3' : cache.CachedValue(_id + "3"),
  '4' : cache.CachedValue(_id + "4"),
  '5' : cache.CachedValue(_id + "5"),
  '6' : cache.CachedValue(_id + "6"),
  '7' : cache.CachedValue(_id + "7"),
  '8' : cache.CachedValue(_id + "8"),
}

def getId():
  return _id

def cmdPrefix():
  return _prefix

def getValue(key=_id):
  if key in cachedValues.keys():
    return cachedValues[key].getValue()
  elif key in (_id):
    return getValues()
  logger.debug("Invalid key: " + key)
  return ''

def waitValue(key=_id, timeout=None):
  if key in cachedValues:
    return cachedValues[key].waitValue(timeout)
  elif key in (_id):
    return waitValues(timeout)
  logger.debug("Invalid key: " + key)
  return ''

def getValues():
  lines = ''
  for key in cachedValues:
    lines += cachedValues[key].getValue() + '\n'
  return lines

def waitValues(timeout=None):
  lines = ''
  for key in cachedValues:
    lines += cachedValues[key].waitValue(timeout) + '\n'
  return lines

def createRequest(request):
  for key in cachedValues:
    cachedValues[key].invalidate()
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
      key = getId() + reply[3]
      text = '' + reply[4:].strip()
      if text is '\x00':
        text = ''
      cachedValues[reply[3]].update(text)
      logger.debug('Processed: ' + text)
      return { key : text}
  return None
