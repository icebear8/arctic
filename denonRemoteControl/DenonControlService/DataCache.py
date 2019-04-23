
import logging

from threading import Event

values = {}

def getValue(key):
  if key in values.keys():
    return str(values[key])
  return ''

class CachedValue:
  def __init__(self, id):
    self._id = id
    self._evtUpdated = Event()

  def update(self, value):
    values[self._id] = value
    self._evtUpdated.set()

  def invalidate(self):
    self._evtUpdated.clear()

  def getValue(self):
    return getValue(self._id)

  def waitValue(self, timeout=None):
    self._evtUpdated.wait(timeout)
    return self.getValue()
