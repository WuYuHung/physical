from django.db import models


class Staff(models.Model):
    class Meta:
        permissions = (
            ("blood", "blood"),
            ("x-ray", "x-ray"),
            ("heart", "heart"),
            ("sight", "sight"),
            ("hear", "hear"),
        )
