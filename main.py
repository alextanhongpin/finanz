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

from usecase.crud_entry.model import Expense

define('port', default=5000, help='the application port')

HEADER_X_REQUEST_ID = 'X-Request-ID'


class MainHandler(RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST']

    def initialize(self):
        pass

    def prepare(self):
        '''This is initialized before every requests.'''
        request_id = self.request.headers.get(HEADER_X_REQUEST_ID)
        if not request_id:
            self.request.headers[HEADER_X_REQUEST_ID] = str(uuid4())

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json; charset=utf-8')

    def get(self):
        request_id = self.request.headers.get(HEADER_X_REQUEST_ID)
        data = {'id': '1', 'amount': 100.0, 'name': 'hello'}
        exp = Expense(**data)
        #  exp = Expense(id='1', amount=100.0, name='hello')
        res = dataclasses.asdict(exp)
        res['request_id'] = request_id
        self.write(json.dumps(res))

    def post(self):
        req = tornado.escape.json_decode(self.request.body)
        self.write(req)


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
    app = Application([
        (r"/", MainHandler),
    ], debug=True)
    server = HTTPServer(app)
    server.listen(options.port)

    signal.signal(SIGTERM, partial(sig_handler, server))
    signal.signal(SIGINT, partial(sig_handler, server))

    print(f'listening to port *:{options.port}. press ctrl + c to cancel')
    IOLoop.current().start()


if __name__ == '__main__':
    main()
