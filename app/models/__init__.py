from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import inspect, orm

from app.extensions import db
from app.libs.utils import camel2line


class MixinJSONSerializer:
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set([column.name for column in columns])
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            try:
                self._fields.remove(key)
            except:
                pass
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)


# 提供软删除，及创建时间，更新时间信息的crud model
class InfoCrud(db.Model, MixinJSONSerializer):
    __abstract__ = True
    id = db.Column(db.BigInteger, primary_key=True)
    create_time = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    update_time = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # delete_time = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self):
        name: str = self.__class__.__name__
        if not hasattr(self, '__tablename__'):
            self.__tablename__ = camel2line(name)

    def to_dict(self, _exclude=None):
        _exclude = _exclude or ['delete_time']
        for key in _exclude:
            self.hide(key)
        kv = []
        for key in set(self._fields):
            val = getattr(self, key)
            if isinstance(val, datetime):
                val = val.strftime('%Y-%m-%dT%H:%M:%SZ')
            kv.append((key, val))
        return dict(kv)

    def _set_fields(self):
        self._exclude = ['delete_time']

    # 硬删除
    def delete(self, commit=False):
        db.session.delete(self)
        if commit:
            db.session.commit()

    # 查
    @classmethod
    def get(cls, start=None, count=None, one=True, **kwargs):
        # 应用软删除，必须带有delete_time
        if kwargs.get('delete_time') is None:
            kwargs['delete_time'] = None
        if one:
            return cls.query.filter().filter_by(**kwargs).first()
        return cls.query.filter().filter_by(**kwargs).offset(start).limit(count).all()

    # 查
    @classmethod
    def list(cls):
        return cls.query.all()

    # 查
    @classmethod
    def get_by_id(cls, _id):
        return cls.query.get(_id)

    # 查
    @classmethod
    def get_and_check_by_id(cls, _id):
        return cls.query.get_or_404(_id)

    # 增
    @classmethod
    def create(cls, **kwargs):
        one = cls()
        for key in kwargs.keys():
            if hasattr(one, key):
                setattr(one, key, kwargs[key])
        db.session.add(one)
        if kwargs.get('commit') is True:
            db.session.commit()
        return one

    def update(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
        db.session.add(self)
        if kwargs.get('commit') is True:
            db.session.commit()
        return self
