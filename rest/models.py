from django.db import models

class Word(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.TextField(blank = True, default = '', null = True)
    accepted = models.BooleanField(default = False)
    corrects = models.IntegerField(null = True, blank = True)
    wrongs = models.IntegerField(null = True, blank = True)
