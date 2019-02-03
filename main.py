import tornado.ioloop
from tornado.options import define, options
import tornado.web
import json
import time
import logging
import signal
from functools import partial

define('port', default=5000, help='the application port')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps({'hello': 'world'}))

    def post(self):
        req = tornado.escape.json_decode(self.request.body)
        self.write(req)


def sig_handler(server, sig, frame):
    instance = tornado.ioloop.IOLoop.instance()

    async def shutdown():
        server.stop()
        logging.info('will shutdown in %s seconds', 3)
        await tornado.gen.sleep(3)
        instance.stop()

    instance.add_callback_from_signal(shutdown)


def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", MainHandler),
    ], debug=True)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)

    signal.signal(signal.SIGTERM, partial(sig_handler, server))
    signal.signal(signal.SIGINT, partial(sig_handler, server))

    print(f'listening to port *:{options.port}. press ctrl + c to cancel')
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
