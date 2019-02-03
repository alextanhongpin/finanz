import tornado
from tornado.web import RequestHandler
import logging
import json
import dataclasses

from .model import Expense


class Controller(RequestHandler):
    SUPPORTED_METHODS = ['GET', 'POST']

    def initialize(self, repo):
        self.repo = repo

    def get(self):
        expenses = self.repo.list()
        res = {'data': expenses}
        self.write(json.dumps(res))

    def post(self):
        #  data = {'id': '1', 'amount': 100.0, 'name': 'hello'}
        try:
            req = tornado.escape.json_decode(self.request.body)
            exp = Expense(**req)
            res = self.repo.create(exp)
            self.write(json.dumps(res))
        except Exception as exc:
            logging.error(exc)
            self.write(json.dumps({'error': 'something happened'}))
