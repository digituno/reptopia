from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.managers import InheritanceManager
from dict.models import Dictionary
import reptopia


class Post(models.Model):
    pub_date = models.DateField(default=timezone.now, blank=False)
    board_type = models.ForeignKey(
                 Dictionary,
                 related_name='board_type',
                 on_delete=models.CASCADE,
                 limit_choices_to={'category': reptopia._BBS_TYPE_},
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    board_status = models.ForeignKey(
                  Dictionary,
                  related_name='board_status',
                  on_delete=models.CASCADE,
                  limit_choices_to={'category': reptopia._BBS_STATUS_},
    )
    created_date = models.DateTimeField(default=timezone.now)

    objects = InheritanceManager()

    def get_absolute_url(self):
        # return reverse('pet-detail', kwargs={'userid': self.owner.pk, 'pk': self.pk})
        return reverse('post-list')


class Notice(Post):
    notice_from_date = models.DateField(default=timezone.now, blank=False)
    notice_to_date = models.DateField(default=timezone.now, blank=False)

