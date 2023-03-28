from django.forms import ModelForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, CustomUser



class RegisterForm(UserCreationForm, ModelForm, forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "identification"]







class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'nationality', 'id_or_passport', 'visa_card_number', 'visa_card_expiry']
        widgets = {
            'id_or_passport': forms.ClearableFileInput(attrs={'multiple': False}),
        }






class CustomUserForm(UserCreationForm, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =['username','email', 'password1', 'password2']





