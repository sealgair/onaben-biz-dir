from django import forms
from directory.models import Business, Address, PhoneNumber, Owner
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory

class BasicBizForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ('name', 
                  'description', 
                  'categories', 
                  'start_date',
                  'date_registered')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('business')

class PhoneForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        exclude = ('business')

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        exclude = ('businesses')

AddressFormset = formset_factory(AddressForm, extra=1, can_delete=False)
PhoneFormset = formset_factory(PhoneForm, extra=1, can_delete=False)
OwnerFormset = formset_factory(OwnerForm, extra=1, can_delete=False)

class BusinessForm(forms.ModelForm):
    name = forms.CharField(label="Business Name")
    description = forms.CharField(widget=forms.Textarea)
    home_based = forms.BooleanField(initial=False)
    full_time_employees = forms.IntegerField(min_value=0, initial=1,
                                             label="Full time employees", 
                                             widget=forms.TextInput(attrs={"class":"number"}))
    part_time_employees = forms.IntegerField(min_value=0, initial=0,
                                             label="Part time employees", 
                                             widget=forms.TextInput(attrs={"class":"number"}))
    other_notes = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Business
        fields = ('name',
                  'website',
                  'email',
                  'description',
                  'full_time_employees',
                  'part_time_employees',
                  'start_date',
                  'sic_or_cert_type',
                  'referred_by',
                  'woman',
                  'minority',
                  'home_based',
                  'nw_region',
                  'email_list',
                  'mailing_list',
                  'categories',
                  'other_notes')
    
    def __init__(self, data = None, *args, **kwargs):
        super(BusinessForm, self).__init__(data, *args, **kwargs)
    
        self.addresses = AddressFormset(data)
        self.phone_numbers = PhoneFormset(data)
        self.owners = OwnerFormset(data)
    
    def clean_categories(self):
        cats = self.cleaned_data['categories']
        
        max_cats = 3
        cat_count = len(cats)
        if cat_count > max_cats:
            raise forms.ValidationError("Too many categories defined (found %s, max is %s)" %
                                        (cat_count, max_cats))
        return cats
    
    def is_valid(self, *args, **kwargs):
        valid = super(BusinessForm, self).is_valid()
        
        valid = valid & self.addresses.is_valid()
        valid = valid & self.phone_numbers.is_valid()
        valid = valid & self.owners.is_valid()
        
        return valid
        
    def save(self, *args, **kwargs):
        biz = super(BusinessForm, self).save(*args, **kwargs)
        
        for addy in self.addresses.save():
            addy.business = biz
            addy.save()
        
        for phone in self.phone_numbers.save():
            phone.business = biz
            phone.save()
        
        for owner in self.owners.save():
            owner.businesses.add(biz)
            owner.save()
