from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    school_name = forms.CharField(max_length=100, required=True, label="Место учебы")
    SCHOOL_TYPE_CHOICES = [
        ('high_school', 'Старшая школа'),
        ('middle_school', 'Средняя школа'),
        ('university', 'Университет'),
        ('other', 'Другое'),
    ]
    school_type = forms.ChoiceField(choices=SCHOOL_TYPE_CHOICES, required=True, label="Тип учебного заведения")
    graduation_date = forms.DateField(required=True, label="Дата выпуска", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'school_name', 'school_type', 'graduation_date', 'password1', 'password2']