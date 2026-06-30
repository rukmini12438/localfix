from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.RadioSelect)
    phone = forms.CharField(max_length=15, required=False)
    location = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'phone', 'location']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone=self.cleaned_data.get('phone', ''),
                location=self.cleaned_data.get('location', ''),
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'location', 'photo', 'bio']
