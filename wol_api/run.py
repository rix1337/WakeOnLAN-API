# -*- coding: utf-8 -*-
# WakeOnLAN-API
# Project by https://github.com/rix1337

import argparse
import multiprocessing
import re
import sys
from socketserver import ThreadingMixIn
from wsgiref.simple_server import make_server, WSGIServer, WSGIRequestHandler

from bottle import Bottle, abort, request
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

        def wake_device(mac):
            try:
                send_magic_packet(mac)
                message = f"Request type: {request.method}, Path: {request.path} | Woke up: {mac}"
                print(message)
                return message
            except Exception as e:
                message = f"Request type: {request.method}, Path: {request.path} | Error: {str(e)}"
                print(message)
                abort(500, message)

        @app.post("/<mac>")
        @app.get("/<mac>")
        @app.post("/wol/<mac>")
        @app.get("/wol/<mac>")
        def status(mac):
            return wake_device(mac)

        print(f"[WakeOnLAN-API] Running at http://127.0.0.1:{shared_state.values['port']}")
        try:
            Server(app, listen='0.0.0.0', port=shared_state.values["port"]).serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
