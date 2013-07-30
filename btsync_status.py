#!/usr/bin/python
import base64
import json
import re
import sys
import time
import urllib2

DEFAULT_SLEEP_INTERVAL = 10
DEFAULT_PROTO = 'http'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8888

config_file = 'config.json'
if len(sys.argv) == 2:
  config_file = sys.argv[1]

try:
  with open(config_file, 'r') as f:
    config = json.loads(f.read())
except IOError, e:
  print "Could not open file %s for reading." % config_file
  sys.exit(1)

proto = config['proto'] if 'proto' in config else DEFAULT_PROTO
host = config['host'] if 'host' in config else DEFAULT_HOST
port = int(config['port']) if 'port' in config else DEFAULT_PORT
sleep_interval = int(config['sleep_interval']) if 'sleep_interval' in config else DEFAULT_SLEEP_INTERVAL

def get_token():
  uri = '/gui/token.html'
  result = get_request(uri)
  if result:
    cookie = result.headers.get('Set-Cookie')
    data = result.read()
    token = re.findall('<div[^>]*>([^>]*)<', data)
    if token:
      return token[0], cookie
  return None, None

def get_request(uri, cookie = None):
  request = urllib2.Request('%s://%s:%d%s' % (proto, host, port, uri))
  if 'username' in config and 'password' in config:
    base64string = base64.encodestring('%s:%s' % (config['username'], config['password'])).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
  if cookie:
    request.add_header('cookie', cookie)

  try:
    return urllib2.urlopen(request)
  except urllib2.URLError, e:
    print "Error with HTTP request: %s." % e
    return None

def get_stats(token, cookie):
  uri = '/gui/?token=%s&action=getsyncfolders' % token
  result = get_request(uri, cookie)
  return json.loads(result.read())

token, cookie = get_token()
if token and cookie:
  while True:
    try:
      print
      stats = get_stats(token, cookie)
      for folder in stats['folders']:
        print "%s: %s" % (folder['name'],folder['size'])
        for peer in folder['peers']:
          arrow_status = " "
          if 'downarrow' in peer['status']:
            arrow_status = u'\u2193 '
          if 'uparrow' in peer['status']:
            arrow_status = arrow_status + u'\u2191 '
          status = re.sub('^.*>\s','',peer['status'])

          print "  %s: %s%s" % (peer['name'], arrow_status, status)
      print stats['speed']
      time.sleep(config['sleep_interval'])
    except KeyboardInterrupt:
      break
else:
  print 'Could not get a token and cookie.'
