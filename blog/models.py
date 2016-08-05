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
            standard_width = 618
            standard_height = 348

            # When a image is smaller than standard image both width and height --> don't do resizing
            if standard_width > self.image_file.width and standard_height > self.image_file.height:
                result_width = self.image_file.width
                result_height = self.image_file.height
            # When a image's width and height is same or width is bigger than height  --> resizing based on width
            elif self.image_file.width >= self.image_file.height:
                weight_width = (standard_width / float(self.image_file.width))
                result_width = standard_width
                result_height = int(float(self.image_file.height) * float(weight_width))
            # When a image's height is bigger than width --> fix ratio of the image based on height
            elif self.image_file.height > self.image_file.width:
                weight_height = (standard_height / float(self.image_file.height))
                result_height = standard_height
                result_width = int(float(self.image_file.width) * float(weight_height))
            else:
                NotImplementedError

            result_size = str(result_width)+'x'+str(result_height)
            resized = get_thumbnail(self.image_file, result_size, quality=85, format='JPEG')
            self.image_file.save(resized.name, ContentFile(resized.read()), True)
        super(Resource, self).save(*args, **kwargs)



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
