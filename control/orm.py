#!/usr/bin/env python
#-*- encoding:utf-8 -*-

class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        mapping = cls.__fields__ # 读取cls的Field字段
        primary_key = cls.__primary_key__# 查找primary_key字段
        __table__ = cls.__talbe__ # 读取cls的__table__字段
        # 给cls增加一些字段：
        attrs['__mapping__'] = mapping
        attrs['__primary_key__'] = primary_key
        attrs['__table__'] = __table__
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMetaClass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

