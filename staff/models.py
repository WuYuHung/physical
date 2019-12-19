from django.db import models


class Staff(models.Model):
    class Meta:
        permissions = (("staff", "staff"),)
