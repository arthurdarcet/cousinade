from django.contrib import admin
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    birth_date = models.DateField()
    picture = models.ImageField(upload_to='pictures')
    father = models.ForeignKey('self', related_name='+', db_column='father_id', blank=True, null=True, on_delete=models.SET_NULL)
    mother = models.ForeignKey('self', related_name='+', db_column='mother_id', blank=True, null=True, on_delete=models.SET_NULL)
    info = models.TextField()

    def children(self):
        return Person.objects.filter(father=self) + Person.objects.filter(mother=self)

admin.site.register(Person)
