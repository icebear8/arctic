
import logging

# Volume module
logger = logging.getLogger(__name__)

def cmdPrefix():
  return 'PW'

def createRequest(request):
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
  if reply.startswith(cmdPrefix()):
    return True
  return False

def processReply(reply):
  if isProcessible(reply) is True:
    logger.debug('Processed: ' + reply[2:])
    return reply[2:]

  return None
