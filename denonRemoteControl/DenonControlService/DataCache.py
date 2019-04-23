
import logging

values = {}

def getValue(key):
  if key in values.keys():
    return str(values[key])
  return ''
