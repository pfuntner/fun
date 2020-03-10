#! /usr/bin/env python3

import os
import re
import json
import logging
import argparse
import requests
import subprocess

class PasswordHider(logging.Formatter):
  """
  This class can be used to hide passwords in native Python logging messages.  A sample usage:
      import logging
      LOG_FORMAT = '%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s'
      logging.basicConfig(format=LOG_FORMAT)
      for handler in logging.root.handlers:
         handler.setFormatter(PasswordHider(LOG_FORMAT))
      log = logging.getLogger('ultralogs')
      log.setLevel(logging.DEBUG)
      obj = {
              'password': 'secret',
              'list': [
                {
                  'PASSWD': 'secret',
                },
              ],
            }
      logg.info(obj)
      logg.info('Password=shhhhhh')
  Sample output:
    2019-02-20 15:00:19,402 INFO ./passlogger:46 {'password': '********', 'list': [{'PASSWD': '********'}]}
    2019-02-20 15:00:19,406 INFO ./passlogger:47 Password=********
  """

  """
    this regular expression finds passwords preceded by the phrases "password" or "passwd".  The single
    subexpression extracted is the password portion.  The caller can substitute anything they like in place
    of the password.
    The password string is just the next set of characters that follows the `password` identifier.  If it's closed with
    quotes, the quotes will remain.  I couldn't find a decent way to allow embedded quotes.  If that's a problem, the
    regular expression can always be revisited.
  """
  regexp = re.compile(
    '(?:PASSWORD|PASSWD|PWD)[\'"]?[ :\t=]*(?:(?:\\\?u?[\'"])?)([-a-zA-Z0-9!@#$%^&*()_+=[\]\\|;:,./<>?]+)',
    re.IGNORECASE)

  # this is the string that will replace all password strings
  replacement_string = '*'*8 # eight asterisks

  def __init__(self, log_format):
    super(PasswordHider, self).__init__(log_format)
    self.passwords = set()

  def _filter(self, s):
    """
    Find all potential occurrences of a password in a string and replace the password with a replacement string
    :param s: A message to be logged
    :return: The message after replacing any passwords
    """

    if not os.environ.get('EXPOSE_PASSWORDS'):
      # we process the hits right to left so we don't disturb the beginning/ending positions of hits further to the right
      for hit in list(self.regexp.finditer(s))[-1::-1]:
        if not hit.group(1).startswith('hider.py:'): # avoid `hiding` my module name
          s = s[:hit.start(1)] + self.replacement_string + s[hit.end(1):]
      for password in self.passwords:
        s = s.replace(password, self.replacement_string)
    return s

  def add_password(self, password):
    """
    Add a password to be obfuscated
    :param password: A password as a string
    :return: None
    """

    self.passwords.add(password)

  def format(self, record):
    """
    Override logging.Formatter.format() to replace password strings
    :param record: The record to send to the log, before formatting
    :return: The post-formatted string with potential passwords replaced by a replacement string.
    """
    original = logging.Formatter.format(self, record)
    return self._filter(original)

def run(cmd):
  if isinstance(cmd, str):
    cmd = cmd.split()
  log.info('Executing {cmd}'.format(**locals()))
  p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = tuple([s.decode('utf-8') for s in p.communicate()])
  # alternately, if trapping is conditional:
  # if trap:
  #   stdout = stdout.decode('utf-8')
  #   stderr = stderr.decode('utf-8')
  rc = p.wait()
  log.debug('Executed {cmd}: {rc}, {stdout!r}, {stderr!r}'.format(**locals()))
  return (rc, stdout, stderr)

def envparse(filename):
  ret = {}
  with open(os.path.expanduser(filename)) as stream:
    for line in stream.readlines():
      match = env_regexp.search(line)
      if match:
        ret[match.group(1)] = match.group(2).strip('\'').strip('"')
        
  return ret

parser = argparse.ArgumentParser(description='Openstack test')
parser.add_argument('-v', '--verbose', action='count', help='Enable debugging')
args = parser.parse_args()

LOG_FORMAT = '%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s'
logging.basicConfig(format=LOG_FORMAT)
for handler in logging.root.handlers:
  handler.setFormatter(PasswordHider(LOG_FORMAT))
log = logging.getLogger()
log.setLevel(logging.WARNING - (args.verbose or 0)*10)

url_regexp = re.compile(r'(http(?:s)?)://([^:/]+)(?::(\d+))?(?:/(.*))?$')

env_regexp = re.compile(r'^\s*(?:export\s+)?(\w+)\s*=\s*(\S+)')
env = envparse("~/sto/runon-rcv3.sh")
log.debug(f'env: {env}')

headers = {"Content-Type": "application/json"}

password = None
(rc, stdout, stderr) = run('SecureKeyValues.py --operation read --store cisco --ssh --json')
if rc == 0 and stdout:
  password = json.loads(stdout).get('pairs', []).get('cec_password')

if not password:
  parser.error('Password required')

"""
curl -v -s -X POST $OS_AUTH_URL/auth/tokens?nocatalog   -H "Content-Type: application/json"   -d '{ "auth": { "identity": { "methods": ["password"],"password": {"user": {"domain": {"name": "'"$OS_USER_DOMAIN_NAME"'"},"name": "'"$OS_USERNAME"'", "password": "'"$OS_PASSWORD"'"} } }, "scope": { "project": { "domain": { "name": "'"$OS_PROJECT_DOMAIN_NAME"'" }, "name":  "'"$OS_PROJECT_NAME"'" } } }}' | json
"""
url = '{OS_AUTH_URL}/auth/tokens?nocatalog'.format(**env)
log.debug(f'auth url: {url!r}')
req = requests.post(
  url,
  data=json.dumps({
         'auth': {
           'identity': {
             'methods': ['password'],
             'password': {
               'user': {
                 'domain': {
                   'name': env['OS_USER_DOMAIN_NAME'],
                 },
                 'name': env['OS_USERNAME'],
                 'password': password,
               },
             },
           },
           'scope': {
             'project': {
               'domain': {
                  'name': env['OS_PROJECT_DOMAIN_NAME'],
               }, 
              'name': env['OS_PROJECT_NAME'],
             },
           },
         },
       }),
  headers=headers,
)

log.debug(f'auth status_code: {req.status_code}')
log.debug(f'auth headers: {req.headers}')
log.debug(f'auth text: {req.text!r}')
if req.ok:
  token = req.headers.get('X-Subject-Token')
  headers['X-Auth-Token'] = token

  match = url_regexp.search(env['OS_AUTH_URL'])
  if match:
    protocol = match.group(1)
    server = match.group(2)
    port = match.group(3)
    path = match.group(4)

    # url = '{OS_AUTH_URL}/{OS_PROJECT_ID}/servers'.format(**env)
    url = '{protocol}://{server}:8774/v2/{OS_PROJECT_ID}/servers/detail'.format(protocol=protocol, server=server, OS_PROJECT_ID=env['OS_PROJECT_ID'])

    log.debug(f'servers url: {url!r}')
    req = requests.get(url, headers=headers)
    log.debug(f'servers status_code: {req.status_code}')
    log.debug(f'servers headers: {req.headers}')
    log.debug(f'servers text: {req.text!r}')
    print(json.dumps(req.json(), indent=2, sort_keys=True))
  else:
    parser.error('Cannot parse {}'.format(env['OS_AUTH_URL']))
