from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils import timezone
from mysite import settings

class Post(models.Model):
    author = models.ForeignKey('authentication.Account')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Resource(models.Model):
#    post = models.ForeignKey('blog.Post', related_name='resources')
    image_file = models.ImageField(upload_to='image/original/%Y/%m/%d')
    filtered_image_file = models.ImageField(null=True, upload_to='image/filtered/%Y/%m/%d')
#    movie_file = models.FileField(null=True, upload_to='movie/%Y/%m/%d')
    external_url = models.TextField(max_length=1024, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def delete(self, *args, **kwargs):
        self.image_file.delete()
        self.filtered_image_file.delete()
 #       self.movie_file.delete()
        super(Resource, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('resource_detail', kwargs={'pk': self.id})


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.ForeignKey('authentication.Account')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class SubComment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='subComments')
    comment = models.ForeignKey('blog.Comment', related_name='subComments')
    author = models.ForeignKey('authentication.Account')
    text = models.TextField()
    created_date= models.DateTimeField(default=timezone.now)

    def approve(self):
        self.save()
