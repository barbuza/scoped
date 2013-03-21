# -*- coding: utf-8 -*-

from django.utils import unittest

from .models import Article, User


class ScopedTestCase(unittest.TestCase):

    def setUp(self):
        
        self.published = Article.objects.create(title="published",
                                                published=True)
        
        self.draft = Article.objects.create(title="draft",
                                            published=False)

        self.with_comments = Article.objects.create(title="with_comments",
                                                    published=True,
                                                    has_comments=True)

        self.with_comments.comment_set.create(title="published",
                                              published=True)

        self.with_comments.comment_set.create(title="published",
                                              published=False)

        self.user = User.objects.create()
        self.user.liked.add(self.published)
        self.user.liked.add(self.with_comments)


    def tearDown(self):

        Article.objects.all().delete()


    def test_scoped(self):
        
        self.assertEqual(self.published.pk,
                         Article.objects.published().first().pk)

        self.assertEqual(self.draft.pk,
                        Article.objects.drafts().first().pk)


    def test_chaining(self):
        
        self.assertEqual(self.with_comments.pk,
                         Article.objects.published().with_comments().first().pk)

        self.assertEqual(None,
                         Article.objects.drafts().with_comments().first())


    def test_related(self):

        self.assertEqual(1,
                         self.with_comments.comment_set.published().count())

        self.assertEqual(2,
                         self.user.liked.count())

        self.assertEqual(1,
                         self.user.liked.with_comments().count())

        self.assertEqual(1,
                         self.published.user_set.count())

        self.assertEqual(0,
                         self.published.user_set.admin().count())
