from django import forms
from .models import Developer
from django.contrib.auth.hashers import make_password

class DeveloperRegisterForm(forms.ModelForm):
    """
    Form for registering a developer.
    """
    class Meta:
        model = Developer
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        """
        Save the developer to the database.
        """
        developer = super().save(commit=False)
        developer.is_developer = True
        developer.password = make_password(self.cleaned_data['password'])
        if commit:
            developer.save()
        return developer

    
class DeveloperLoginForm(forms.Form):
    """
    Form for logging in a developer.
    """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)