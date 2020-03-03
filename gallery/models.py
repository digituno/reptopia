from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
import reptopia


class Photo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/%Y/%m/%d')
    title = models.CharField(blank=True, max_length=200)
    desc = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()

    def __str__(self):
        return '[' + self.desc+ ']';

    def get_absolute_url(self):
        return reverse('photo-list')

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)
    
    def get_model_name(self):
        return Pet.__name__
