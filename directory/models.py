from datetime import datetime, date

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
    
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
    
    name = models.CharField(max_length=64)
    
    def get_absolute_url(self):
        return reverse('one', kwargs={'show_by': 'category', 
                                      'name': urlquote(self.name)})
    
    def __unicode__(self):
        return self.name
    
    def alpha(self):
        return self.name.upper()[0]

MODERATION_TYPES = (('Pending', 'Pending'),
                    ('Approved', 'Approved'),
                    ('Rejected', 'Rejected'))

class Business(models.Model):
    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ["name"]
        
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(null=True, default=None, blank=True)
    email = models.EmailField(null=True, default=None, blank=True)
    description = models.TextField(default='')
    
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(null=True, blank=True)
    home_based = models.BooleanField(default=True)
    full_time_employees = models.IntegerField(default=1)
    part_time_employees = models.IntegerField(default=0)
    
    nw_region = models.BooleanField(default=True)
    woman = models.BooleanField(default=False)
    minority = models.BooleanField(default=False)
    sic_or_cert_type = models.CharField(max_length=64, null=True, blank=True)
    
    email_list = models.BooleanField(default=False)
    mailing_list = models.BooleanField(default=False)
    contact_for_marketing = models.BooleanField(default=False)
    
    referred_by = models.CharField(max_length=64, blank=True)
    still_operating = models.BooleanField(default=False)
    will_publish = models.BooleanField(default=False)
    will_advertise = models.BooleanField(default=False)
    
    date_registered = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    
    ready_to_print = models.BooleanField(default=False)
    publish_online = models.BooleanField(default=False)
    other_notes = models.CharField(max_length=512, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="businesses", blank=True)
    
    moderation = models.CharField(max_length=16, null=False, 
                                  choices = MODERATION_TYPES,
                                  default = 'Pending')
    
    def get_absolute_url(self):
        return reverse('one', kwargs={'show_by': 'business', 
                                      'name': urlquote(self.name)})
    
    def safe_email(self):
        #if self.email == None: return ""
        return self.email.replace("@", " (AT) ").replace(".", " (DOT) ")
    
    def alpha(self):
        return self.name.upper()[0]
    
    def __unicode__(self):
        return self.name

class Owner(models.Model):
    business = models.ForeignKey(Business, related_name="owners", null=True, blank=False)
    tribe = models.BooleanField(default=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    title = models.CharField(max_length=64, null=True, blank=True, default=None)
    onaben_client = models.BooleanField(default=False)
    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)

ADDY_TYPES = (('Mailing','Mailing'),
              ('Physical','Physical'),
              ('Mailing & Physical','Mailing & Physical'))
class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"
    business = models.ForeignKey(Business, related_name="addresses")
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=16)
    country_outside_us = models.CharField(max_length=64, null=True, blank=True)
    addy_type = models.CharField(max_length=64, default='Mailing & Physical', choices=ADDY_TYPES)
    do_not_publish_addy = models.BooleanField(default=True)
    def __unicode__(self):
        return self.street

PHONE_TYPES = (("Phone","Phone"),
               ("Fax","Fax"),
               ("Phone & Fax","Phone & Fax"),
               ("Cell","Cell"),
               ("Toll Free","Toll Free"),
               )

class PhoneNumber(models.Model):
    business = models.ForeignKey(Business, related_name="phone_numbers")
    phone_type = models.CharField(max_length=32, null=True, default="Phone", choices=PHONE_TYPES)
    phone_number = models.CharField(max_length=16)
    extension = models.CharField(max_length=32, null=True, blank=True)
    def __unicode__(self):
        return self.phone_number
