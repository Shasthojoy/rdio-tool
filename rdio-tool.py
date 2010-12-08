#!/usr/bin/env python

import sys, os, json
sys.path.append(os.path.join(os.path.dirname(__file__), 'python-oauth2'))
from optparse import OptionParser
from rdio import Rdio

parser = OptionParser(usage='%prog [options] method arg1=value1 arg2=value2...', version='%prog 0.1')
parser.add_option('--consumer-key', dest='consumer_key', help='the consumer key to use for this and future requests', metavar='KEY')
parser.add_option('--consumer-secret', dest='consumer_secret', help='the consumer secret to use for this and future requests', metavar='SECRET')
parser.add_option('--authenticate', dest='authenticate', help='authenticate against Rdio before making the request', action='store_true', default=False)
parser.add_option('--forget-auth', dest='forget_auth', help='discard previous authentication information', action='store_true', default=False)
parser.add_option('-v', '--verbose', dest='verbose', help='verbose output', action='store_true', default=False)


(options, args) = parser.parse_args()

if len(args) < 1:
  parser.print_help()
  sys.exit(1)

config_path = os.path.expanduser('~/.rdio-tool.json')
if os.path.exists(config_path):
  config = json.load(file(config_path))
else:
  config = {'auth_state': {}}
  
if options.consumer_key is not None:
  config['consumer_key'] = options.consumer_key
if options.consumer_secret is not None:
  config['consumer_secret'] = options.consumer_secret

if not config.has_key('consumer_key') or not config.has_key('consumer_secret'):
  sys.stderr.write('Both the consumer key and consumer secret must be specified')
  sys.exit(1)
  
rdio = Rdio(config['consumer_key'], config['consumer_secret'], config['auth_state'])

method = args.pop(0)
args = dict([a.split('=',1) for a in args])
result = rdio.call(method, **args)
json.dump(result, sys.stdout, indent=True)
sys.stdout.write('\n')

f = file(config_path, 'w')
json.dump(config, f, indent=True)
f.write('\n')