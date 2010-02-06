from django import forms
from onaben.directory.models import *

class BusinessForm(forms.ModelForm):
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