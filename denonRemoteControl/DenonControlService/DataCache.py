
import logging

from threading import Event

_valueStorage = {}

def getValue(key):
  if key in _valueStorage.keys():
    return str(_valueStorage[key].getValue())
  return ''

def waitValue(key, timeout=None):
  if key in _valueStorage.keys():
    return str(_valueStorage[key].waitValue(timeout))
  return ''

class CachedValue:
  def __init__(self, id):
    self._id = id
    self._evtUpdated = Event()
    self._value = None
    if self._id not in _valueStorage.keys():
      _valueStorage[id] = self

  def update(self, value):
    self._value = value
    self._evtUpdated.set()

  def invalidate(self):
    self._evtUpdated.clear()

  def getValue(self):
    return str(self._value)

  def waitValue(self, timeout=None):
    self._evtUpdated.wait(timeout)
    return str(self._value)
