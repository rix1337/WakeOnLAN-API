# -*- coding: utf-8 -*-
# WakeOnLAN-API
# Project by https://github.com/rix1337

"""WakeOnLAN-API.

Usage:
  web.py        [--port=<PORT>]

Options:
  --port=<PORT>             Set the listen port
"""

from docopt import docopt
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from wakeonlan import send_magic_packet


def app_container(port):
    app = Flask(__name__)

    @app.route("/wol/<mac>", methods=['POST'])
    def myjd_stop(mac):
        if request.method == 'POST':
            try:
                send_magic_packet(mac)
                print("Waking up: " + mac)
                return "Success", 200
            except:
                return "Failed", 400
        else:
            return "Failed", 405

    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()


def main():
    arguments = docopt(__doc__, version='WakeOnLAN-API')

    if arguments['--port']:
        port = int(arguments['--port'])
    else:
        port = 8080
    app_container(port)
