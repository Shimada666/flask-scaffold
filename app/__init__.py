# -*- coding: utf-8 -*-

import json
import time

from flask import Flask, request, g

from app.commands import register_commands
from app.exceptions import APIException, HTTPException
from app.extensions import db, cors
from app.libs.web_response import WebResponse


def import_module(mod_name):
    """ 导入模块 """
    try:
        return __import__(mod_name, fromlist=[''])
    except ImportError as e:
        print(e)


def create_app(env='test'):
    app = Flask(__name__, static_url_path='/')
    app.config['ENV'] = env

    app.config.from_object(f'app.config.{env}.Config')

    register_before_request(app)
    register_after_request(app)

    register_extensions(app)
    register_commands(app)
    register_errors(app)

    register_routes(app)

    return app


def register_routes(app):
    import pkgutil
    from app import controller
    with app.app_context():
        for _, name, _ in pkgutil.iter_modules(controller.__path__):
            mod_name = f'{controller.__name__}.{name}'
            mod = import_module(mod_name)
            print(f'loading route: {mod_name:20} =>    {"ok" if mod else "failed"}')


def register_before_request(app):
    @app.before_request
    def request_cost_time():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)


def register_after_request(app):
    @app.after_request
    def log_response(resp):
        if not app.config.get('LOG_ENABLE_REQUEST_LOG'):
            return resp
        message = f'[{request.method}] -> [{request.path}] from:{request.remote_addr} costs:{float(g.request_time()) * 1000:.2f} ms '
        if app.config.get('LOG_LEVEL') == 'INFO':
            app.logger.info(message)
        elif app.config.get('LOG_LEVEL') == 'DEBUG':
            req_body = '{}'
            try:
                req_body = request.get_json() if request.get_json() else {}
            except:
                pass
            message += " data:{\n\tparam: %s, \n\tbody: %s\n} " % (
                json.dumps(request.args, ensure_ascii=False),
                req_body
            )
            app.logger.debug(message)
        return resp


def register_extensions(app):
    db.init_app(app)
    cors.init_app(app, supports_credentials=True)


def register_errors(app):
    @app.errorhandler(Exception)
    def handler(e):
        if isinstance(e, APIException):
            return WebResponse.build_error(e.code, e.msg)
        if isinstance(e, HTTPException):
            return WebResponse.build_error(10001, e.description)
        else:
            if not app.config['DEBUG']:
                return WebResponse.build_error(10001, 'unknown error')
            else:
                raise e
