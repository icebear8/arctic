
import logging
import DataCache as cache

logger = logging.getLogger(__name__)

_id = 'volume'
_prefix = 'MV'
cachedValue = cache.CachedValue(_id)

def getId():
  return _id

def cmdPrefix():
  return _prefix

def getValue():
  return cachedValue.getValue()

def waitValue(timeout=None):
  return cachedValue.waitValue(timeout)

def createRequest(request):
  cachedValue.invalidate()
  request = request.upper()

  if request in ('GET'):
    return cmdPrefix() + '?\r'
  elif request in ('UP', 'DOWN'):
    return cmdPrefix() + request + '\r'
  elif request.isdecimal() is True:
    return cmdPrefix() + request[:2] + '\r'

  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  if reply.startswith(cmdPrefix()):
    return True
  return False

def processReply(reply):
  if isProcessible(reply) is True:
    if reply[2:].isdecimal() is True:
        cachedValue.update(reply[2:4])
        logger.debug('Processed: ' + reply[2:])
        return reply[2:4]

  return None
