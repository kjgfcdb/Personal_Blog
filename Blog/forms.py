from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    passwd = forms.CharField(max_length=50)


class BlogForm(forms.Form):
    name = forms.CharField(max_length=50)
    summary = forms.CharField(max_length=200)
    content = forms.CharField()
