import pdb
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from account.forms import CodeForm
from account.models import Account, UserAccount
from location.models import Zip
from punchcode.models import Reward, EarnedReward
from retailer.models import Retailer
from tools import geocode

class RegisterForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(label='E-mail')
    zip = forms.IntegerField(label='Zip Code')
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(max_value=99)
    sex = forms.ChoiceField(choices = (('Male', 'M'), ('Female', 'F')))

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
            exists = User.objects.get(username=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']

        raise forms.ValidationError('Email is already in use')

    def save(self):

        user = User.objects.create_user(username=self.cleaned_data['email'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        account = UserAccount()
        account.user = user
        user.profile = account
        user.save()

        account.age = self.cleaned_data['age']
        account.gender = self.cleaned_data['sex']
        account.zip = self.cleaned_data['zip']

        account.save()
        return user


class MobileCodeForm(forms.Form):
    access_token = forms.CharField()
    expires = forms.IntegerField()
    employee_username = forms.CharField()
    retailer_id = forms.IntegerField()
    retailer_password = forms.CharField()

class MobileConfirmFBPostForm(forms.Form):
    access_token = forms.CharField()
    expires = forms.IntegerField()
    retailer_id = forms.IntegerField()

class MobileSearchForm(forms.Form):
    method = forms.CharField()
    lng = forms.FloatField()
    lat = forms.FloatField()
    distance = forms.IntegerField()
    address = forms.CharField()
    zip = forms.IntegerField()

class MobileUserSearchForm(forms.Form):
    search = forms.CharField()

class MobileAccessTokenForm(forms.Form):
    access_token = forms.CharField()
    expires = forms.IntegerField()

class MobileRewardInfoForm(forms.Form):
    reward_id = forms.IntegerField()

    def clean_reward_id(self):
        rewardID = self.cleaned_data['reward_id']
        try:
            reward_obj = Reward.objects.get(pk=rewardID)
        except Reward.DoesNotExist:
            raise forms.ValidationError('Reward does not exist')

        return rewardID

class MobileRetailerInfoForm(forms.Form):
    retailer_id = forms.IntegerField()

    def clean_retailer_id(self):
        retailerID = self.cleaned_data['retailer_id']
        try:
            retailer_obj = Retailer.objects.get(pk=retailerID)
        except Retailer.DoesNotExist:
            raise forms.ValidationError('Retailer does not exist')

        return retailerID

class MobileRedeemRewardForm(forms.Form):
    user_id = forms.IntegerField()
    earned_reward_id = forms.IntegerField()
    password = forms.CharField()

    def clean_user_id(self):
        id = self.cleaned_data['user_id']
        try:
            user_obj = UserAccount.objects.get(pk=id)
        except UserAccount.DoesNotExist:
            raise forms.ValidationError('User does not exist')

        return user_obj

    def clean_earned_reward_id(self):
        id = self.cleaned_data['earned_reward_id']
        try:
            earned_reward_obj = EarnedReward.objects.get(pk=id)
        except EarnedReward.DoesNotExist:
            raise forms.ValidationError('Reward does not exist')

        return earned_reward_obj

class MobileAdminRedeemRewardForm(forms.Form):
    employee_username = forms.CharField()
    earned_reward_id = forms.IntegerField()
    retailer_id = forms.IntegerField()
    retailer_password = forms.CharField()
    access_token = forms.CharField()
    expires = forms.IntegerField()

class MobileAdminLoginForm(forms.Form):
    retailer_id = forms.IntegerField()
    username = forms.CharField()
    password = forms.CharField()

class MobileUserIDForm(forms.Form):
    user_id = forms.IntegerField()

