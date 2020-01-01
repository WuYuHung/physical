from django import forms
from patient.models import Task

class HomeForm(forms.ModelForm):  

    class Meta:
        model = Task
        fields = ('patient', 'kind',)
        
