
import logging

# Volume module
logger = logging.getLogger(__name__)

def getId():
  return 'volume'

def cmdPrefix():
  return 'MV'

def createRequest(request):
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
        logger.debug('Processed: ' + reply[2:])
        return { getId() : reply[2:4] }

  return None
