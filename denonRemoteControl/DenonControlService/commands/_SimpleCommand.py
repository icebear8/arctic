
import logging
import DataCache as cache

def isProcessible(prefix, reply):
  if reply.startswith(prefix):
    return True
  return False

def processReply(prefix, reply, cachedValue):
  if isProcessible(prefix, reply) is True:
    startIdx = len(prefix)
    cachedValue.update(reply[startIdx:])
    return reply[startIdx:]
  return None
