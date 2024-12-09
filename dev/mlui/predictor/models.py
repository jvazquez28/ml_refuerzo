# mlui/predictor/models.py

from django.db import models

class Prediction(models.Model):
    region = models.IntegerField()
    tenure = models.IntegerField()
    age = models.IntegerField()
    marital = models.IntegerField()
    address = models.IntegerField()
    income = models.FloatField()
    ed = models.IntegerField()
    employ = models.IntegerField()
    retire = models.FloatField()
    gender = models.IntegerField()
    reside = models.IntegerField()
    prediction = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'predictions'