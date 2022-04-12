# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Genre(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Video(models.Model):
    key = models.CharField(primary_key=True,max_length=15)
    name = models.CharField(max_length=255,blank=True)
    genre = models.ForeignKey(Genre,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.key + " "+ self.genre.name

