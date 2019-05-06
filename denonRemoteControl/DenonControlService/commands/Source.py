
import logging
import DataCache as cache
import commands._SimpleCommand as cmdSimple

logger = logging.getLogger(__name__)

_id = 'source'
_prefix = 'SI'
_requests = [ 'TUNER', 'DVD', 'BD', 'TV', 'SAT/CBL', 'GAME', 'AUX1', 'FLICKR',
    'MPLAY', 'NET', 'PANDORA', 'SIRIUSXM', 'SPOTIFY', 'FAVORITES', 'IRADIO', 'SERVER', 'USB/IPOD',
    'USB', 'IPD', 'IRP', 'FVP'
]
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
  elif request in (_requests):
    return cmdPrefix() + request + '\r'
  elif request in ('SATCBL'):
    return cmdPrefix() + 'SAT/CBL' + '\r'
  elif request in ('USBIPOD'):
    return cmdPrefix() + 'USB/IPOD' + '\r'

  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  return cmdSimple.isProcessible(cmdPrefix(), reply)

def processReply(reply):
  return cmdSimple.processReply(cmdPrefix(), reply, cachedValue)
