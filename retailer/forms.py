from datetime import datetime
import pdb
from django import forms
from django.contrib.auth.models import User, UserManager
from django.forms.models import ModelForm
from retailer.models import RegistrationCode, RetailerUpdate
from location.models import Zip, City
from punchcode.models import Reward
from retailer.models import NewRetailerContact, Retailer
from tools import geocode, build_address

class RetailerContactForm(ModelForm):
    class Meta:
        model = NewRetailerContact
        exclude = ('date')

    def save(self):
        contact = super(RetailerContactForm, self).save(commit=False)
        contact.date = datetime.now()
        contact.save()
        return contact

class NewRetailerForm(ModelForm):
    zip = forms.IntegerField()
    city = forms.CharField()

    class Meta:
        model = Retailer
        fields = ('name', 'description','hours','category','address','zip','city','phone','admin_password')

    def clean_zip(self):
        zipobj, created = Zip.objects.get_or_create(code=self.cleaned_data['zip'])
        return zipobj

    def clean_city(self):
        if type(self.cleaned_data['zip']) != type(Zip()):
            self.clean_zip(self)

        try:
            cityobj = City.objects.get(name=self.cleaned_data['city'], zip__pk__in=[self.cleaned_data['zip'].pk,])
        except City.DoesNotExist:
            cityobj = City()
            cityobj.name = self.cleaned_data['city']
            cityobj.save()
            cityobj.zip.add(self.cleaned_data['zip'])
            cityobj.save()
        return cityobj


    def save(self, commit=True):
        retailer = super(NewRetailerForm, self).save(commit=True)
        reg_code = RegistrationCode()
        reg_code.code = str(hash(str(retailer.name)+str(datetime.now())))[1:20]
        reg_code.save()
        retailer.registration_code = reg_code

        update = RetailerUpdate(action='join', retailer=retailer)
        update.save()
        retailer.updates.add(update)

        retailer.save()
        return retailer

    def save_m2m(self):
        try:
            super(NewRetailerForm, self).save_m2m()
        except:
            pass


class EditRetailerForm(ModelForm):

    zip = forms.IntegerField()
    city = forms.CharField()

    class Meta:
        model = Retailer
        fields = ('name', 'description', 'hours', 'category', 'phone', 'address', 'city', 'zip', 'main_image')

    def clean(self):
        cleaned_data = super(EditRetailerForm, self).clean()
        zip = cleaned_data.get('zip')
        city = cleaned_data.get('city')

        if zip and city:
            try:
                cityobj = City.objects.get(name=city, zip__pk__in=[zip.pk,])
            except City.DoesNotExist:
                cityobj = City()
                cityobj.name = city
                cityobj.save()
                cityobj.zip.add(zip)
                cityobj.save()

            cleaned_data['city'] = cityobj

        return cleaned_data


    def clean_zip(self):
        zipobj, created = Zip.objects.get_or_create(code=self.cleaned_data['zip'])
        return zipobj



class RewardForm(ModelForm):
    class Meta:
        model = Reward
        fields = ('punches', 'text')


class SearchForm(forms.Form):
    address = forms.CharField()



