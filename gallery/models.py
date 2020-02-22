from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import reptopia


class Photo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/%Y/%m/%d')
    desc = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '[' + self.desc+ ']';

    """
    def get_absolute_url(self):
        return reverse('pet-detail', kwargs={'userid': self.owner.pk, 'pk': self.pk})
    """

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)
