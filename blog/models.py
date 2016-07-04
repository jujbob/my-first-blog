from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils import timezone


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
    post = models.ForeignKey('blog.Post', related_name='resources')
    image_file = models.ImageField(upload_to='image/post/original/%Y/%m/%d')
    filtered_image_file = models.ImageField(null=True, upload_to='image/post/filtered/%Y/%m/%d')
    movie_file = models.FileField(null=True, upload_to='movie/post/%Y/%m/%d')
    external_url = models.TextField(max_length=1024, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def delete(self, *args, **kwargs):
        self.image_file.delete()
        self.filtered_image_file.delete()
        self.movie_file.delete()
        super(Resource, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('resource_detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if not self.id:
            super(Resource, self).save(*args, **kwargs)
            standard_width = 600
            standard_height = 300
            weight_width = (standard_width / float(self.image_file.width))
            result_width = standard_width
            result_height = int(float(self.image_file.height) * float(weight_width))
            result_size = str(result_width)+'x'+str(result_height)

            resized = get_thumbnail(self.image_file, result_size, quality=85, format='JPEG')
            self.image_file.save(resized.name, ContentFile(resized.read()), True)
        super(Resource, self).save(*args, **kwargs)

#            self.image_file = get_thumbnail(self.image_file, '100x100', quality=85, format='JPEG')
            #super(Resource, self).save(*args, **kwargs)

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
