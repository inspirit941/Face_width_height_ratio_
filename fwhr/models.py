from django.db import models
from django.utils import timezone


class Image(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField()
    gender = models.CharField(max_length=10)
    age = models.IntegerField(default=20)
    fwhr = models.FloatField(default=0.)
    country = models.CharField(max_length=10)
    ethnicity = models.CharField(max_length=10)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    occupation = models.TextField(null=True)
    ip = models.TextField(null=True)
    face_coord = models.TextField(null=True)

    def __str__(self):
        return str(self.age) + ", " + self.gender + ", " + self.country + ", " + \
            self.ethnicity + ", " + str(self.fwhr)

class MS_API(models.Model):
    created_date = models.DateTimeField(default = timezone.now)
    # faceid = models.TextField(null=True)
    image = models.ImageField()
    gender = models.CharField(max_length = 10)
    age = models.IntegerField(default = 0)
    smiles = models.FloatField(default = 0.)
    # emotions
    anger = models.FloatField(default=0.)
    contempt = models.FloatField(default=0.)
    disgust = models.FloatField(default=0.)
    fear = models.FloatField(default=0.)
    happiness = models.FloatField(default=0.)
    neutral = models.FloatField(default=0.)
    sadness = models.FloatField(default=0.)
    surprise = models.FloatField(default=0.)
    # 대머리정도
    bald = models.FloatField(default=0.)
    # 얼굴 수염
    moustache = models.FloatField(default=0.)
    beard = models.FloatField(default=0.)
    sideburns = models.FloatField(default=0.)