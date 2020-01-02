from django import forms
from patient.models import Task
from django.forms.widgets import CheckboxSelectMultiple


class HomeForm(forms.ModelForm):
    OPTIONS = (
        ("抽血", "抽血"),
        ("心電圖", "心電圖"),
        ("X光", "X光"),
        ("視力檢查", "視力檢查"),
        ("聽力檢查", "聽力檢查"),
    )
    kind = forms.MultipleChoiceField(
        required=True, widget=CheckboxSelectMultiple(), choices=OPTIONS
    )

    class Meta:
        model = Task
        fields = ("patient", "kind")
        widgets = {
            "myfield": forms.TextInput(
                attrs={
                    "style": "padding:5px 15px; border:2px black solid;cursor:pointer;-webkit-border-radius: 5px;border-radius: 5px;"
                }
            )
        }
