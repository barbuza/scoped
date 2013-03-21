# -*- coding: utf-8 -*-

import functools

from django.db import models
from django.contrib.auth.models import AbstractBaseUser


__all__ = ("ScopedModel", "ScopedManager", "ScopedQuerySet",
           "ScopedBase", )


class ScopedQuerySet(models.query.QuerySet):

    def first(self):
        lst = list(self[:1])
        return lst[0] if lst else None

    def __getattr__(self, attr, *args):
        try:
            super(ScopedQuerySet, self).__getattr__(attr, *args)
        except AttributeError:
            method = getattr(self.model.Scopes, attr)
            curried = functools.partial(method, self)
            functools.update_wrapper(curried, method)
            return curried


class ScopedManager(models.Manager):

    use_for_related_fields = True

    def get_query_set(self):
        return ScopedQuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith("__"):
            raise AttributeError
        try:
            return super(ScopedManager, self).__getattr__(attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class ScopedBase(models.base.ModelBase):

    def __new__(cls, name, bases, dct):
        if name != "ScopedModel":
            if bases[0] is ScopedModel and "objects" not in dct:
                dct.update(objects=ScopedManager())
        if "Scopes" not in dct:
            raise RuntimeError("%s must have Scopes declared" % name)
        return models.base.ModelBase.__new__(cls, name, bases, dct)


class ScopedModel(models.Model):

    __metaclass__ = ScopedBase

    class Meta:
        abstract = True

    class Scopes:
        pass


