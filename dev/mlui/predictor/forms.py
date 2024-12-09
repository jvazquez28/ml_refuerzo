# mlui/predictor/forms.py
from django import forms

class SinglePredictionForm(forms.Form):
    region = forms.IntegerField()
    tenure = forms.IntegerField()
    age = forms.IntegerField()
    marital = forms.IntegerField()
    address = forms.IntegerField()
    income = forms.FloatField()
    ed = forms.IntegerField()
    employ = forms.IntegerField()
    retire = forms.FloatField()
    gender = forms.IntegerField()
    reside = forms.IntegerField()

class FileUploadForm(forms.Form):
    file = forms.FileField()