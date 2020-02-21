from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Post(models.Model):
    pub_date = models.DateField(default=timezone.now, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        # return reverse('pet-detail', kwargs={'userid': self.owner.pk, 'pk': self.pk})
        return reverse('post-list')
