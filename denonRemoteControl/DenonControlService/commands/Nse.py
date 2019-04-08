
import logging

# Volume module
logger = logging.getLogger(__name__)

def cmdPrefix():
  return 'NSE'

def createRequest(request):
  request = request.upper()

  if request in ('GET'):
    return cmdPrefix() + '\r'

  logger.debug('Ignore unknwon request')
  return None

def isProcessible(reply):
  if reply.startswith(cmdPrefix()):
    return reply[3].isdecimal()
  return False

def processReply(reply):
  if isProcessible(reply) is True:
      text = '' + reply[4:].strip()
      if text is '\x00':
        text = ''
      logger.debug('Processed: ' + text)
      return {int(reply[3]) : text}

  return None
