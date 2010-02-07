from django.db import models, connection
from datetime import datetime

class AdvancedManager(models.Manager):
    """
    """
    
    def search(self, search=""):
        data = self.get_query_set()
        if not search:
            return data
        
        q = models.Q()
        for f in self.model.search_fields():
            q = q | models.Q(**{f+"__icontains":search})
        return data.filter(q)
    
    def alpha(self, letter=""):
        data = self.get_query_set()
        if not letter:
            return data
        
        return data.filter(name__istartswith = letter)
    
    def alphabet(self):
        cursor = connection.cursor()
        query = "SELECT DISTINCT UPPER(SUBSTRING(name,1,1)) FROM {table} order by name;".format(table = self.model._meta.db_table)
        cursor.execute(query)
        alphabet = [a[0] for a in cursor.fetchall()]
        return alphabet
    
    def alpha_index(self, letter="A", search=""):
        data = self.search(search)
        return data.filter(name__lt=letter).count()
    
class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]
    
    objects = AdvancedManager()
    
    name = models.CharField(max_length=64)
    
    @staticmethod
    def search_fields():
        return ['name']
    
    def name_url(self):
        return name_to_url(self.name)
    
    def __unicode__(self):
        return self.name
    
    def alpha(self):
        return self.name.upper()[0]

class Owner(models.Model):
    tribe = models.BooleanField(default=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    title = models.CharField(max_length=64, null=True, default=None)
    onaben_client = models.BooleanField(default=False)
    def __unicode__(self):
        return "%s, %s" % (self.last_name, self.first_name)

class Business(models.Model):
    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ["name"]
        
    objects = AdvancedManager()
       
    name = models.CharField(max_length=255, unique=True)
    nw_region = models.BooleanField(default=True)
    website = models.URLField(null=True, default=None)
    email = models.EmailField(null=True, default=None)
    description = models.CharField(max_length=2000, default='')
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    home_based = models.BooleanField(default=True)
    full_time_employees = models.IntegerField(default=1)
    part_time_employees = models.IntegerField(default=0)
    woman = models.BooleanField(default=False)
    minority = models.BooleanField(default=False)
    sic_or_cert_type = models.CharField(max_length=64, null=True)
    email_list = models.BooleanField(default=False)
    mailing_list = models.BooleanField(default=False)
    contact_for_marketing = models.BooleanField(default=False)
    referred_by = models.CharField(max_length=64)
    still_operating = models.BooleanField(default=False)
    will_publish = models.BooleanField(default=False)
    will_advertise = models.BooleanField(default=False)
    date_registered = models.DateField() 
    last_updated = models.DateField(default=datetime.now())
    ready_to_print = models.BooleanField(default=False)
    publish_online = models.BooleanField(default=False)
    other_notes = models.CharField(max_length=512, null=True)
    categories = models.ManyToManyField(Category)
    owners = models.ManyToManyField(Owner)
    
    def nameField(self):
        return "name"
    
    @staticmethod
    def search_fields():
        return ['name']
        return ['name', 'website', 'email', 'description', 'owner__first_name', 'owner__last_name']
    def name_url(self):
        return name_to_url(self.name)
    def safe_email(self):
        #if self.email == None: return ""
        return self.email.replace("@", " (AT) ").replace(".", " (DOT) ")
    def alpha(self):
        return self.name.upper()[0]
    def __unicode__(self):
        return self.name

ADDY_TYPES = (('Mailing','Mailing'),
              ('Physical','Physical'),
              ('Mailing & Physical','Mailing & Physical'))
class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"
    business = models.ForeignKey(Business)
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=16)
    country_outside_us = models.CharField(max_length=64, null=True, default=None)
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
    business = models.ForeignKey(Business)
    phone_type = models.CharField(max_length=32, null=True, default="Phone", choices=PHONE_TYPES)
    phone_number = models.CharField(max_length=16)
    extension = models.CharField(max_length=32, null=True, default=None)
    def __unicode__(self):
        return self.phone_number

url_reps = [('%','%25'),
            ('$','%24'),
            ('&','%26'),
            ('+','%2B'),
            (',','%2C'),
            ('/','%2F'),
            (':','%3A'),
            (';','%3B'),
            ('=','%3D'),
            ('?','%3F'),
            ('@','%40'),
            (' ','%20'),
            ('"','%22'),
            ('<','%3C'),
            ('>','%3E'),
            ('#','%23')]
def name_to_url(name):
    url = name
    for char, code in url_reps:
        url = url.replace(char, code)
    return url
def name_from_url(url):
    name = url
    for char, code in url_reps:
        name = name.replace(code, char)
    return name