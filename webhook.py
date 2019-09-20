#! /usr/bin/env python2

"""
Borrowed from https://gist.github.com/bradmontgomery/2219997

An attempt to create a git webhook but a pre-receive hook might be more useful.
"""

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

import json
import logging

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<html><body><h1>hi!</h1></body></html>")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_POST(self):
        log.info('path: {self.path}'.format(**locals()))
        log.info('headers: {}'.format(repr(str(self.headers))))
        content_length = int(self.headers.getheaders('content-length')[0])
        log.info('content length: {content_length}'.format(**locals()))
        req = self.rfile.read(content_length)
        log.info('request: {req!r}'.format(**locals()))

        self.send_response(404)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(json.dumps(['Posssssssst']))
        
def run(server_class=HTTPServer, handler_class=RequestHandler, port=80):
    log.info('Starting httpd with port {port}...'.format(**locals()))
    httpd = server_class(('', port), handler_class)
    httpd.serve_forever()

logging.basicConfig(format='%(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(msg)s')
log = logging.getLogger()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='simple git webhook server')
    parser.add_argument('-p', '--port', type=int, default=8080, help='Server port')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Enable debugging')
    args = parser.parse_args()

    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    run(port=args.port)
