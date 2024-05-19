# -*- coding: utf-8 -*-
# WakeOnLAN-API
# Project by https://github.com/rix1337

import argparse
import multiprocessing
import re
import sys
from socketserver import ThreadingMixIn
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

from bottle import Bottle
from wakeonlan import send_magic_packet

from wol_api.providers import shared_state, version


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass


class Server:
    def __init__(self, wsgi_app, listen='127.0.0.1', port=8080):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(self.listen, self.port, self.wsgi_app,
                                  ThreadingWSGIServer, handler_class=NoLoggingWSGIRequestHandler)

    def serve_forever(self):
        self.server.serve_forever()


def main():
    with multiprocessing.Manager() as manager:
        shared_state_dict = manager.dict()
        shared_state_lock = manager.Lock()
        shared_state.set_state(shared_state_dict, shared_state_lock)

        print("[WakeOnLAN-API] Version " + version.get_version() + " by rix1337")
        shared_state.update("ready", False)

        parser = argparse.ArgumentParser()
        parser.add_argument("--port", help="Desired Port, defaults to 8080")
        arguments = parser.parse_args()

        if arguments.port:
            try:
                shared_state.update("port", int(arguments.port))
            except ValueError:
                print("[WakeOnLAN-API] Port must be an integer")
                sys.exit(1)
        else:
            shared_state.update("port", 8080)

        app = Bottle()

        @app.post("/<mac>")
        def status(mac):
            mac = mac.replace("-", ":").strip()
            # Validate MAC address
            if not re.match("^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac):
                print("Invalid MAC address: " + mac)
                return "Invalid MAC address", 400

            # Wake up device
            try:
                print("Waking up: " + mac)
                send_magic_packet(mac)
                return "Success", 200
            except Exception as e:
                print(f"Failed to wake up device: {e}")
                return "Failed", 500

        print(f"[WakeOnLAN-API] Running at http://127.0.0.1:{shared_state.values['port']}")
        try:
            Server(app, listen='0.0.0.0', port=shared_state.values["port"]).serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
