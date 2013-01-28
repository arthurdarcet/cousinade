from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='pictures', blank=True, null=True)
    father = models.ForeignKey('self', related_name='+', db_column='father_id', blank=True, null=True, on_delete=models.SET_NULL)
    mother = models.ForeignKey('self', related_name='+', db_column='mother_id', blank=True, null=True, on_delete=models.SET_NULL)
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

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)
