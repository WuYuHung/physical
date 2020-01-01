from django.db import models


class Patient(models.Model):
    class Meta:
        permissions = (("patient", "patient"),)


class Task(models.Model):
    patient = models.CharField(max_length=20, help_text="病人ID")
    kind = models.CharField(max_length=20, help_text="種類 ex. 抽血")
    start_time = models.DateTimeField(help_text="起始時間")
    doctor = models.CharField(max_length=20, help_text="醫生ID")
