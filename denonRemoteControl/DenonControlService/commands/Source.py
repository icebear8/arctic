
import logging
import DataCache as cache
import commands._SimpleCommand as cmdSimple

logger = logging.getLogger(__name__)

_id = 'source'
_prefix = 'SI'
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

  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  return cmdSimple.isProcessible(cmdPrefix(), reply)

def processReply(reply):
  return cmdSimple.processReply(cmdPrefix(), reply, cachedValue)
