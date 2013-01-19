import pdb
import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.forms import widgets
from django.forms.models import ModelForm
from account.models import Account, UserAccount, RetailerAccount, Employee
from retailer.models import RegistrationCode
from location.models import Zip
from punchcode.models import Code, Punch
from tools import geocode

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput)
        
class FacebookRegisterForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    zip = forms.IntegerField()
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=( ('male','male'),('female','female') ))

    def clean_zip(self):
        try:
            zip = Zip.objects.get(code=self.cleaned_data['zip'])
        except Zip.DoesNotExist:
            zip = Zip()
            location = geocode(self.cleaned_data['zip'])
            zip.lng = location['lng']
            zip.lat = location['lat']
            zip.code = self.cleaned_data['zip']
            zip.save()
        return zip

    def save(self):
        email = self.cleaned_data['email']
        try:
            user = UserAccount.objects.get(email=email)
        except UserAccount.DoesNotExist:
            user = UserAccount()
            first_name = self.cleaned_data['name'].split()[0]
            last_name = self.cleaned_data['name'].split()[1]
            password = self.cleaned_data['password']
            user.first_name = first_name
            user.last_name = last_name
            user.username = email
            user.email = email
            user.set_password(password)
            user.zip = self.cleaned_data['zip']
            user.gender = self.cleaned_data['gender']
            user.save()

        return user


class UserRegisterForm(ModelForm):
    def __init__(self, *args, **kw):
        super(ModelForm, self).__init__(*args, **kw)
        self.fields.keyOrder = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'zip',
            'age',
            'sex'
        ]

    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'zip', 'age', 'sex')

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    zip = forms.IntegerField(label='Zip Code')
    sex = forms.ChoiceField(choices = (('M', 'Male'), ('F', 'Female')))

    def clean_confirm_password(self):
        if self.cleaned_data['confirm_password'] == '':
            raise forms.ValidationError('Please confirm your password')

        if self.cleaned_data['password'] and self.cleaned_data['confirm_password']:
            if self.cleaned_data['password'] == self.cleaned_data['confirm_password']:
                return self.cleaned_data['password']

        raise forms.ValidationError('Passwords must match')

    def clean_zip(self):
        try:
            zip = Zip.objects.get(code=self.cleaned_data['zip'])
        except Zip.DoesNotExist:
            zip = Zip()
            location = geocode(self.cleaned_data['zip'])
            zip.lng = location['lng']
            zip.lat = location['lat']
            zip.code = self.cleaned_data['zip']
            zip.save()
        return zip

    def clean_email(self):
        try:
            exists = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']

        raise forms.ValidationError('Email is already in use')

    def save(self):
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']
        user.type = 'user'

        user.save()
        return user


class RetailerRegisterForm(ModelForm):
    class Meta:
        model = RetailerAccount
        fields = ('email', 'phone' )

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        retailer_account = super(RetailerRegisterForm, self).save(commit=False)
        retailer_account.set_password(self.cleaned_data['password'])
        retailer_account.username = self.cleaned_data['email']
        retailer_account.type = 'retailer'

        if commit:
            retailer_account.save()

        return retailer_account


class RetailerRegistrationCodeForm(forms.Form):
    registration_code = forms.CharField()

    def clean_registration_code(self):
        code = self.cleaned_data['registration_code']

        try:
            registration_code = RegistrationCode.objects.get(pk=code)
        except RegistrationCode.DoesNotExist:
            raise forms.ValidationError('Invalid Code')

        return registration_code
        
class CodeForm(forms.Form):
    punchcode = forms.CharField(label="Enter re:punch code")

    def clean_punchcode(self):
        try:
            code = Code.objects.get(code=self.cleaned_data['punchcode'].strip())
        except Code.DoesNotExist:
            raise forms.ValidationError('Invalid Code')

        if code.used:
            raise forms.ValidationError('Code has been used')

        return code

    def save(self, commit=True):
        code = self.cleaned_data['punchcode']

        code.used = True
        if commit:
            code.save()
        return code

class EditAccountForm(ModelForm):
    class Meta:
        model = UserAccount
        fields = ('zip', 'facebook_post_method')

    def __init__(self, *args, **kwargs):
        super(EditAccountForm, self).__init__(*args, **kwargs)
        self.fields['facebook_post_method'].help_text="Choose how you want us to post to your facebook wall";


    zip = forms.CharField(label="Zip Code", help_text="Enter your zipcode to help us find stores near you")

    def clean_zip(self):
        try:
            zip = Zip.objects.get(code=self.cleaned_data['zip'])
        except Zip.DoesNotExist:
            zip = Zip(code=self.cleaned_data['zip'])
            location = geocode(self.cleaned_data['zip'])
            zip.lng = location['lng']
            zip.lat = location['lat']
            zip.save()
        return zip



class NewEmployeeForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()


