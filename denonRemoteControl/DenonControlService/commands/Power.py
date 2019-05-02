
import logging
import DataCache as cache
import commands._SimpleCommand as cmdSimple

logger = logging.getLogger(__name__)

_id = 'power'
_prefix = 'PW'
cachedValue = cache.CachedValue(_id)

def getId():
  return _id

def cmdPrefix():
  return _prefix

def createRequest(request='get'):
  cachedValue.invalidate()
  request = request.upper()

  if request in ('GET'):
    return cmdPrefix() + '?\r'
  elif request in ('ON'):
    return cmdPrefix() + 'ON\r'
  elif request in ('STANDBY', 'OFF'):
    return cmdPrefix() + 'STANDBY\r'

  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  return cmdSimple.isProcessible(cmdPrefix(), reply)

def processReply(reply):
  return cmdSimple.processReply(cmdPrefix(), reply, cachedValue)
