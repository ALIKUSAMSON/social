from django import forms
from .models import Comment, Post


class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required=False,widget=forms.Textarea())


class CommentForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	body = forms.CharField(required=False,widget=forms.Textarea())

class LikeForm(forms.Form):
	created = forms.DateField(required=False)

class UploadBlogForm(forms.Form):
	title = forms.CharField(max_length=250)
	body = forms.CharField(required=True,widget=forms.Textarea())


class UploadForm(forms.ModelForm):
	class meta:
		model = Post
		fields = ('title', 'body')