import logging
import DataCache as cache

import commands.Source as cmdSource
import commands.Nse as cmdNse

logger = logging.getLogger(__name__)

_id = 'playing'

_cachedValues = {
  'artist' : cache.CachedValue("artist"),
  'title' : cache.CachedValue("title"),
  'album' : cache.CachedValue("album")
}

def getId():
  return _id

def createRequest(request='get'):
  for key in _cachedValues:
    _cachedValues[key].invalidate()
  cmdRequest = cmdSource.createRequest()
  cmdRequest += cmdNse.createRequest()
  return cmdRequest

def evaluate(timeout=None):
  source = cache.waitValue(cmdSource.getId(), timeout)
  if not _isPlayingSource(source):
    _clearValues()
    return
  cache.waitValue(cmdNse.getId() + '8')
  _evaluateValues()

def _isPlayingSource(source):
  return source in ('MPLAY', 'NET', 'SPOTIFY', 'FAVORITES', 'IRADIO', 'SERVER', 'USB/IPOD')

def _clearValues():
  _cachedValues['title'].update('')
  _cachedValues['artist'].update('')
  _cachedValues['album'].update('')

def _evaluateValues():
  if (cache.getValue('line0').startswith("Now Playing")):
    _cachedValues['title'].update(cache.getValue('line1'))
    _cachedValues['artist'].update(cache.getValue('line2'))
    _cachedValues['album'].update(cache.getValue('line4'))
  else:
    _clearValues()
