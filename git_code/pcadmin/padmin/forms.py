from multiselectfield import MultiSelectFormField
from django import forms

class MyForm(forms.ModelForm):
    my_field = MultiSelectFormField(choices=MyModel.MY_CHOICES)