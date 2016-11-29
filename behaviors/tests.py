from django.test import TestCase

from .models import BlogPost


class BehaviorTestCaseMixin(object):
    def get_model(self):
            return getattr(self, 'model')

    def create_instance(self, **kwargs):
        raise NotImplementedError("Implement me")


class PublishableTests(BehaviorTestCaseMixin):
    def test_published_blogpost(self):
        from django.utils import timezone
        obj = self.create_instance(publish_date=timezone.now())
        self.assertTrue(obj.is_published)
        self.assertIn(obj, self.model.objects.published())


class PreBlogPostTestCase(TestCase):
    def test_published_blogpost(self):
        from django.utils import timezone
        blogpost = BlogPost.objects.create(publish_date=timezone.now())
        self.assertTrue(blogpost.is_published)
        self.assertIn(blogpost, BlogPost.objects.published())


class BlogPostTestCase(PublishableTests, TestCase):
    model = BlogPost

    def create_instance(self, **kwargs):
        return BlogPost.objects.create(**kwargs)