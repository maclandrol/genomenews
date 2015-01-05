from django import forms
from news.models import UserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm
from news.models import UserProfile

class RegistrationForm(ModelForm):
    """A class for User registration

    """
    username = forms.CharField(label=(u"Username"))
    email = forms.EmailField(label=(u"Email"), required=False)
    password = forms.CharField(label=(u"Password"), widget=forms.PasswordInput(render_value=False))
    password1= forms.CharField(label=(u"Verify Password"), widget=forms.PasswordInput(render_value=False))

    class Meta:
        model=UserProfile
        # We want to exclude karma, biography and creation date from registration form
        exclude=("user","karma", "biography","created_at")

    def clean_username(self):
        username=self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        # Raise error if user already exists
        raise forms.ValidationError("Username already taken !")

    def clean(self):
        """Clean form data

        """
        password = self.cleaned_data["password"]
        password1 = self.cleaned_data["password1"]
        # Here we verify the chosen password
        if(password != password1):
            raise forms.ValidationError("Password does not match !")
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """User detail page view

    """
    email = forms.EmailField(label=(u"Email"), required=False)

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        # This extend the default constructor to add at the same time
        # User fields and UserProfile fields
        # Add the email field from the user (and not userprofile)
        self.fields['email'].initial = self.instance.user.email

        self.fields.keyOrder = [
            'email',
            ]

    class Meta:
        model = UserProfile
        fields = ('email', "biography",)

    def clean_email(self):
        """Clean email from form

        """
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        # Email shouldn't already be taken
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.email = self.cleaned_data.get('email')
        # We save the User instance in order to update the email field in profile
        self.instance.user.save()
