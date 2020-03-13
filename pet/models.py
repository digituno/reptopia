from django.db import models
from django.conf import settings
from dict.models import Dictionary, AnimalDictionary
from django.utils import timezone
from django.urls import reverse
from django.utils.formats import localize
from taggit.managers import TaggableManager
import reptopia

class Pet(models.Model):
    species = models.ForeignKey(AnimalDictionary, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    gender = models.ForeignKey(
        Dictionary,
        related_name='gender',
        on_delete=models.CASCADE,
        limit_choices_to={'category': reptopia._GENDER_},
    )
    bod = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='pet/%Y/%m/%d', blank=True, null=True)
    desc = models.TextField(blank=True)

    created_date = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()

    def __str__(self):
        return '[' + self.species.common_name_kor + ']' + self.name;

    def get_absolute_url(self):
        return reverse('pet-detail', kwargs={'userid': self.owner.pk, 'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.tags.clear()
        super(Pet, self).delete(*args, **kwargs)

    def get_model_name(self):
        return Pet.__name__


class Feeding(models.Model):
    eat_type = models.ForeignKey(
        Dictionary,
        related_name='eat_type',
        on_delete=models.CASCADE,
        default=21
    )
    prey_type = models.ForeignKey(
        Dictionary,
        related_name='prey_type',
        on_delete=models.CASCADE,
    )
    prey_size = models.ForeignKey(
        Dictionary,
        related_name='prey_size',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    prey_weight = models.IntegerField(blank=True, null=True)
    prey_quantity = models.IntegerField(default=1)


class Care(models.Model):
    date = models.DateField(default=timezone.now, blank=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    type = models.ForeignKey(
        Dictionary,
        related_name='care_type',
        on_delete=models.CASCADE,
        limit_choices_to={'category': reptopia._CARE_},
    )
    weight = models.IntegerField(null=True)
    feeding = models.ForeignKey(
        Feeding,
        on_delete=models.CASCADE,
        null=True
    )
    image = models.ImageField(upload_to='care/%Y/%m/%d', blank=True, null=True)
    desc = models.TextField(blank=True)
    created_datetime = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.pet.name + " : " + localize(self.date) + " : " + self.type.item

    def delete(self, *args, **kwargs):
        self.image.delete()
        if self.feeding:
            self.feeding.delete()
        super(Care, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pet-detail', kwargs={'userid': self.pet.owner.pk, 'pk': self.pet.pk})
