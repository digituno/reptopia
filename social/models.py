from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.conf import settings


class LikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(like__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(like__lt=0)

    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('like')).get('like__sum') or 0


class Like(models.Model):
    _LIKE_ = 1
    _DISLIKE_ = -1

    LIKES = (
        (_DISLIKE_, 'Dislike'),
        (_LIKE_, 'Like')
    )

    like = models.SmallIntegerField(choices=LIKES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeManager()
