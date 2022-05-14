from django import forms
import datetime
from .models import Style


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class PayForm(forms.Form):
    lessons = forms.ModelChoiceField(queryset=Style.objects.all(),
                                     help_text='Выберите стиль танца')
    count_of_lessons = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                          help_text='Введите количество занятий, за которые вы хотите заплатить')
    cost = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                              help_text='Введите сумму, которую хотите заплатить')

