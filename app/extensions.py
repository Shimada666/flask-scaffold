# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import BaseQuery
from app.exceptions import APINotFoundException
from flask_cors import CORS
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):

    def filter_by(self, soft=False, **kwargs):
        # soft 应用软删除
        if soft:
            kwargs['delete_time'] = None
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if not rv:
            raise APINotFoundException()
        return rv

    def first_or_404(self):
        rv = self.first()
        if not rv:
            raise APINotFoundException()
        return rv


db = SQLAlchemy(query_class=Query)
cors = CORS()
