from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PimaIndianDiabetic(models.Model):
    Pregnancies = models.FloatField()
    Glucose = models.FloatField()
    BloodPressure = models.FloatField()
    SkinThickness = models.FloatField()
    Insulin = models.FloatField()
    BMI = models.FloatField()
    DiabetesPedigreeFunction = models.FloatField()
    Age = models.FloatField()
    Outcome = models.IntegerField()

    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    added_date = models.DateTimeField(default=timezone.now)

class PersonalHealthProfile(models.Model):
    Pregnancies = models.FloatField()
    Glucose = models.FloatField()
    Insulin = models.FloatField()
    BMI = models.FloatField()
    Age = models.FloatField()
    Prediction = models.CharField(max_length=255, default=None)

    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    added_date = models.DateTimeField(default=timezone.now)

