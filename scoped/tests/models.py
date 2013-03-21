# -*- coding: utf-8 -*-

from django.db import models

from ..models import ScopedModel


class Article(ScopedModel):

    title = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    has_comments = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Scopes:

        @staticmethod
        def published(qs):
            return qs.filter(published=True)

        @staticmethod
        def drafts(qs):
            return qs.filter(published=False)

        @staticmethod
        def with_comments(qs):
            return qs.filter(has_comments=True)

    class Meta:
        ordering = ("pk", )


class Comment(ScopedModel):

    article = models.ForeignKey(Article)
    title = models.CharField(max_length=255)
    published = models.BooleanField(default=False)

    class Scopes:

        @staticmethod
        def published(qs):
            return qs.filter(published=True)


class User(ScopedModel):

    is_admin = models.BooleanField(default=False)
    liked = models.ManyToManyField(Article)

    class Scopes:
        
        @staticmethod
        def admin(qs):
            return qs.filter(is_admin=True)

