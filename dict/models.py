from django.db import models
import reptopia


class Dictionary(models.Model):
    category = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    item_name = models.CharField(max_length=100, default="")
    item_name_en = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_usable = models.BooleanField(default=True)

    def __str__(self):
        return self.item_name


class AnimalDictionary(models.Model):
    class_name = models.ForeignKey(
        Dictionary,
        related_name='class_name',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Dictionary,
        related_name='order',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    family = models.ForeignKey(
        Dictionary,
        related_name='family',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    genus = models.ForeignKey(
        Dictionary,
        related_name='genus',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    species = models.CharField(max_length=100)
    common_name = models.CharField(max_length=100)
    common_name_kor = models.CharField(max_length=100)
    cites_appendices = models.ForeignKey(
        Dictionary,
        related_name='cites_appendices',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'category': reptopia._CITES_APPENDICES_},
    )
    eating = models.ForeignKey(
        Dictionary,
        related_name='eating',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        limit_choices_to={'category': reptopia._EATING_},
    )

    def __str__(self):
        return self.common_name_kor
