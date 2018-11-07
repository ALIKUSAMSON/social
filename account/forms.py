from django import forms 
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm

Sex = (
		("Male","Male"),
		("Female","Female"),
	)

class LoginForm(forms.Form):
	username = forms.CharField(label='Username or Email')
	password = forms.CharField(label='Password',widget=forms.PasswordInput)


class UserRegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=25)
	email = forms.EmailField()
	password = forms.CharField(label='Password',widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

	def clean_email(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')

		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		return email

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data('email')

		if commit:
			user.save()
		return user


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name', 'email')


class ProfileEditForm(forms.ModelForm):
	sex = forms.CharField(label='Select', widget=forms.Select(choices=Sex))
	class Meta:
		model = Profile
		fields = ('date_of_birth', 'photo')
