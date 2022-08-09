from django import forms
from . import models
class SearchForm(forms.Form):
    PRICE_CHOICES = (
        ('-100000', "10만원 이하"),
        ('100000-300000', "10~30이하"),
        ('300000-500000', "30~50이하"),
        ('500000', "50이상"),

    )
    keyword=forms.CharField(max_length=50, required=False)
    price = forms.MultipleChoiceField(choices=PRICE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    brands= forms.ModelMultipleChoiceField(
        queryset=models.Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )