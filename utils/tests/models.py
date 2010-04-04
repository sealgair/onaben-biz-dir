"""
Models for testing alpha utilities
"""

from django.db import models

class TestModel(models.Model):
    name = models.CharField(max_length=20)
    test = models.CharField(max_length=20, null=True)