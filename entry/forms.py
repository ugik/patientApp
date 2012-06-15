from django import forms
from django.forms import ModelForm
from entry.models import Patient, Entry
from django.contrib.auth.models import User

class RegistrationForm(ModelForm):
    name                   = forms.CharField(label=(u'User Name'))
    email                   = forms.EmailField(label=(u'Email Address'))
    password             = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password1           = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    
    class Meta:
        model = Patient
        exclude = ('user',)

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            User.objects.get(username=name)
        except User.DoesNotExist:
            return name
        raise forms.ValidationError('That username is already take, please select another name')
        
    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password1'):
            raise forms.ValidationError("The passwords did not match. Please try again.")
        return self.cleaned_data

class EntryForm(ModelForm):
    entry                    = forms.CharField(label=(u'Entry'))
    description           =  forms.CharField(label=(u'Description'), widget=forms.Textarea)

    class Meta:
        model = Entry
        exclude = ('patient',)

class LoginForm(forms.Form):
    name                   = forms.CharField(label=(u'User Name'))
    password             = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))


