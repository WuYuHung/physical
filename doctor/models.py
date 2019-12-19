from django.db import models


class Doctor(models.Model):
    class Meta:
        permissions = (("doctor", "doctor"),)
