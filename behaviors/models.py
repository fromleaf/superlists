from django.db import models
from django.contrib.auth.models import User
from .behaviors import Authorable, Permalinkable, Timestampable, Publishable

from .querysets import BlogPostQuerySet

class PreBlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    slug = models.SlugField()
    author = models.ForeignKey(User, related_name='posts')
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True)


class BlogPost(Authorable, Permalinkable, Timestampable, Publishable, models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    objects = BlogPostQuerySet

    @property
    def is_published(self):
        from django.utils import timezone
        return self.publish_date < timezone.now()

    @models.permalink
    def get_absolute_url(self):
        return ('blog-post', (), {
            "slug": self.slug,
        })

    def pre_save(self, instance, add):
        from django.utils.text import slugify
        if not instance.slug:
            instance.slug = slugify(self.title)