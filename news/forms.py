from django import forms
from news.models import UserProfile
from django.contrib.auth.models import User
from django.forms import ModelForm
from news.models import UserProfile, Post


class RegistrationForm(ModelForm):
    """A class for User registration.

    """
    username = forms.CharField(label=(u"Username"))
    email = forms.EmailField(label=(u"Email"), required=False)
    password = forms.CharField(
        label=(u"Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password1 = forms.CharField(
        label=(u"Verify Password"),
        widget=forms.PasswordInput(render_value=False)
    )

    class Meta:
        model = UserProfile
        # We want to exclude karma, biography and creation date from
        # registration form
        exclude = ("user", "karma", "biography", "created_at")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        # Raise error if user already exists
        raise forms.ValidationError("Username already taken !")

    def clean(self):
        """Clean form data.

        """
        email = self.cleaned_data["email"]
        # Test if password is provided
        try:
            password = self.cleaned_data["password"]
            password1 = self.cleaned_data["password1"]
        except KeyError:
            raise forms.ValidationError("Password not provided")
        # Here we verify the chosen password.
        if(password != password1):
            raise forms.ValidationError("Password does not match !")
        # Here we verify if the email is already taken.
        if email and len(User.objects.filter(email=email)) > 0:
            raise forms.ValidationError(
                'This email address is already taken.'
                ' Please supply a different email'
                ' address.'
            )
        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    """User detail page form.

    """

    email = forms.EmailField(label=(u"Email"), required=False)

    class Meta:
        model = UserProfile
        fields = ('email', "biography",)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # This extends the default constructor to add at the same time
        # User fields and UserProfile fields
        # Add the email field from the user (and not userprofile)
        self.fields['email'].initial = self.instance.user.email

        self.fields.keyOrder = ['email']

    def clean_email(self):
        """Clean email from form

        """
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        email_changed = email != self.instance.user.email
        if email and email_changed:
            # The new email should not be in the database.
            if len(User.objects.filter(email=email)) > 0:
                raise forms.ValidationError(
                    'This email address is already in use.'
                    ' Please supply a different email'
                    ' address.'
                )
        return email

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.email = self.cleaned_data.get('email')
        # We save the User instance in order to update the email field in
        # profile
        self.instance.user.save()


class PostForm(forms.ModelForm):
    """Post submission form.

    """
    url = forms.URLField(label=(u"url"), required=False)
    description = forms.CharField(
        label=(u"description"),
        required=False,
        widget=forms.Textarea
        )

    class Meta:
        model = Post
        exclude = ("owner", "rank", "karma")

    def clean(self):
        """Clean PostForm data.

        """
        try:
            # Title is a required field
            title = self.cleaned_data["title"]
        except KeyError:
            raise forms.ValidationError("You must provide a title!")

        url = self.cleaned_data["url"]
        description = self.cleaned_data["description"]
        # A post cannot be a self post and a link post at the same time
        if (description and url) :
            raise forms.ValidationError(
                'You can\'t submit a self post and a link post'
                ' at the same time.'
                ' If you keep the url, post your text as a comment'
                ' in the thread.'
            )
        return self.cleaned_data
