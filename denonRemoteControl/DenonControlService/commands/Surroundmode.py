
import logging
import DataCache as cache
import commands._SimpleCommand as cmdSimple

logger = logging.getLogger(__name__)

_id = 'surround'
_prefix = 'MS'
_requests = [ 'MOVIE', 'MUSIC', 'GAME', 'PURE DIRECT', 'DIRECT', 'STEREO', 'STANDARD', 'DOLBY DIGITAL', 'DTS SUROUND',
  'MCH STEREO', 'ROCK ARENA', 'JAZZ CLUB', 'MONO MOVIE', 'MATRIX', 'VIDEO', 'VIRTUAL'
]

cachedValue = cache.CachedValue(_id)

def getId():
  return _id

def cmdPrefix():
  return _prefix

def createRequest(request='get'):
  cachedValue.invalidate()
  request = request.upper()

  request = request.replace('_', ' ')

  if request in ('GET'):
    return cmdPrefix() + '?\r'
  elif request in (_requests):
    return cmdPrefix() + request + '\r'

  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  return cmdSimple.isProcessible(cmdPrefix(), reply)

def processReply(reply):
  return cmdSimple.processReply(cmdPrefix(), reply, cachedValue)
