"""
"""
from datetime import date

from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.contrib.admin import widgets
from django.template import Context, loader

from directory.models import Category, Business, Address, PhoneNumber, Owner

class ExtraInlineFormset(BaseInlineFormSet):
    """
    """
    min_num = 1
    
    def clean(self):
        """
        """
        if len([d for d in self.cleaned_data if len(d) > 0]) < self.min_num:
            raise forms.ValidationError("%s or more %s required" % (self.min_num, self.prefix))
        
        return super(ExtraInlineFormset, self).clean()
    
    def as_ul(self):
        """
        """
        t = loader.get_template('formset_ul.html')
        c = Context({'formset': self})
        return t.render(c)


class AddressForm(forms.ModelForm):
    do_not_publish_addy = forms.BooleanField(label="Do not publish address", required=False, initial=False)
    country_outside_us = forms.CharField(label="Country (if outside U.S.)", required=False)
    class Meta:
        model = Address
        exclude = ('business')

class PhoneForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        exclude = ('business')

class OwnerForm(forms.ModelForm):
    tribe = forms.BooleanField(label="Tribe Member", required=False)
    onaben_client = forms.BooleanField(label="ONABEN Member", required=False)
    class Meta:
        model = Owner
        fields = ('first_name',
                  'last_name',
                  'title',
                  'tribe',
                  'onaben_client',
                 )
        

AddressFormset = inlineformset_factory(Business, Address, form=AddressForm, 
                                       formset=ExtraInlineFormset,
                                       extra=1, can_delete=False)
PhoneFormset = inlineformset_factory(Business, PhoneNumber, form=PhoneForm, 
                                     formset=ExtraInlineFormset,
                                     extra=2, can_delete=False)
OwnerFormset = inlineformset_factory(Business, Owner, form=OwnerForm, 
                                     formset=ExtraInlineFormset,
                                     extra=1, can_delete=False)

class BusinessForm(forms.ModelForm):
    name = forms.CharField(label="Business Name")
    description = forms.CharField(widget=forms.Textarea)
    start_date = forms.DateField(widget=widgets.AdminDateWidget, initial=date.today())
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), required=False,
                                                label="Categories (please select no more than three)",
                                                widget=widgets.FilteredSelectMultiple("Categories", True))
    class Meta:
        model = Business
        fields = ('name',
                  'description',
                  'website',
                  'email', 
                  'start_date',
                  'categories',
                  'full_time_employees',
                  'part_time_employees',
                  'sic_or_cert_type',
                  'home_based',
                 )
    
    inlines = [OwnerFormset, AddressFormset, PhoneFormset, ]
    
    def clean_categories(self):
        data = self.cleaned_data['categories']
        if len(data) > 3:
            raise forms.ValidationError("Please select no more than three categories")

        return data
    
    def __init__(self, *args, **kwargs):
        self.formsets = {}
        for formset_class in self.inlines:
            prefix = formset_class.get_default_prefix()
            self.formsets[prefix] = formset_class(prefix=prefix, *args, **kwargs)
        return super(BusinessForm, self).__init__(*args, **kwargs)
    
    def is_valid(self, *args, **kwargs):
        
        valid =  super(BusinessForm, self).is_valid(*args, **kwargs)
        for subform in self.formsets.values():
            valid = valid and subform.is_valid(*args, **kwargs)
        return valid
        
    def save(self, *args, **kwargs):
        biz = super(BusinessForm, self).save(*args, **kwargs)
        
        for subform in self.formsets.values():
            subform.instance = biz
            subform.save(*args, **kwargs)
        
        return biz

