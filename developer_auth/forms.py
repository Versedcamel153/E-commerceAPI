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

class DeveloperUpdateForm(forms.ModelForm):
    """
    Form for updating developer profile.
    """
    class Meta:
        model = Developer
        fields = ['username', 'email']

class DeveloperPasswordChangeForm(forms.Form):
    """
    Form for changing developer password.
    """
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Incorrect current password.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

    def save(self):
        new_password = self.cleaned_data['new_password']
        self.user.set_password(new_password)
        self.user.save()
        return self.user