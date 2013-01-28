# coding: utf-8
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone, formats
from lib.thumbs import ImageWithThumbsField


class Person(models.Model):
    TITLE_MISS = 1
    TITLE_MRS = 2
    TITLE_MR = 3
    TITLES = (
        (TITLE_MISS, 'Mademoiselle'),
        (TITLE_MRS, 'Madame'),
        (TITLE_MR, 'Monsieur'),
    )
    TITLES_SHORT = (
        (TITLE_MISS, 'Mlle'),
        (TITLE_MRS, 'Mme'),
        (TITLE_MR, 'M.'),
    )
    PICTURE_THUMBNAILS = ((50,50), (200,200), (400,400))

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    maiden_name = models.CharField(max_length=100, blank=True, null=True)
    title = models.IntegerField(choices=TITLES)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    phone2 = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=200, blank=True, null=True)
    picture = ImageWithThumbsField(upload_to='pictures', sizes=PICTURE_THUMBNAILS, blank=True, null=True)
    father = models.ForeignKey(
        'self',
        related_name='+',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        db_column='father_id',
        limit_choices_to={'title': TITLE_MR},
    )
    mother = models.ForeignKey(
        'self',
        related_name='+',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        db_column='mother_id',
        limit_choices_to={'title__in': (TITLE_MRS, TITLE_MISS)},
    )
    info = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True)
    last_login = models.DateTimeField(default=timezone.now)


    def children(self):
        return Person.objects.filter(father=self) + Person.objects.filter(mother=self)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        if not raw_password:
            return False
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=['password'])
        return check_password(raw_password, self.password, setter)

    def birth(self):
        bdate = formats.date_format(self.birth_date, 'SHORT_DATE_FORMAT') if self.birth_date else None
        if bdate and self.birth_place:
            return '{} à {}'.format(bdate, self.birth_place)
        return bdate or '−'

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)
