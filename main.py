from functools import partial
from signal import SIGTERM, SIGINT
from uuid import uuid4
import dataclasses
import json
import logging
import signal
import time

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options, parse_command_line
from tornado.web import Application, RequestHandler
import tornado

from usecase.crud_expense import make_usecase

define('port', default=5000, help='the application port')

HEADER_X_REQUEST_ID = 'X-Request-ID'


# Convert this into a decorator method.
def request_id(f):
    def decorate(self, *args, **kwargs):
        request_id = self.request.headers.get(HEADER_X_REQUEST_ID)
        if not request_id:
            self.request.headers[HEADER_X_REQUEST_ID] = str(uuid4())
        f(self, *args, **kwargs)

    return decorate


def sig_handler(server, sig, frame):
    instance = IOLoop.instance()

    async def shutdown():
        server.stop()
        logging.info('will shutdown in %s seconds', 3)
        await tornado.gen.sleep(3)
        instance.stop()

    instance.add_callback_from_signal(shutdown)


def main():
    parse_command_line()
    app = Application([make_usecase()], debug=True)
    server = HTTPServer(app)
    server.listen(options.port)

    signal.signal(SIGTERM, partial(sig_handler, server))
    signal.signal(SIGINT, partial(sig_handler, server))

    logging.info('listening to port *:%d. press ctrl + c to cancel',
                 options.port)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
