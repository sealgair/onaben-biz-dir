from django.contrib import admin
from directory.models import Address, Owner, PhoneNumber, Business, Category

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1
class OwnerInline(admin.StackedInline):
    model = Owner
    extra = 1
class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1

class BusinessAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_registered'
    fieldsets = (
                 (None,
                      {'fields': ('name', 'description', ('website', 'email',), ('categories', 'owners'))}),
                 ('Operating info',
                      {'classes': ('collapse',),
                       'fields': (('start_date', 'end_date'), ('full_time_employees', 'part_time_employees'),
                                  ('home_based', 'still_operating'), 'sic_or_cert_type')
                       }),
                 ('Demographic info',
                      {'classes': ('collapse',),
                       'fields': (('nw_region', 'woman', 'minority'),)
                       }),
                 ('Privacy info',
                      {'classes': ('collapse',),
                       'fields': (('email_list', 'mailing_list', 'contact_for_marketing', 'publish_online',),)
                       }),
                 ('Internal info',
                      {'classes': ('collapse',),
                       'fields': ('referred_by', 'other_notes', 
                                  ('ready_to_print','will_publish','will_advertise'))
                       }),
                )
    inlines = [AddressInline, PhoneNumberInline]
    #raw_id_fields = ("categories","owners")
    
    'date_registered',
    'last_updated',
    
admin.site.register(Business, BusinessAdmin)
admin.site.register(Owner)
admin.site.register(Category)
