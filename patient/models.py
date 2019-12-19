from django.db import models


class Patient(models.Model):
    class Meta:
        permissions = (("patient", "patient"),)
