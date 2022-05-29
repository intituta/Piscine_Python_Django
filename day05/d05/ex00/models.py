from operator import mod
from django.db import models


class Bb(models.Model):
	text = models.CharField(max_length=50)
# Create your models here.
