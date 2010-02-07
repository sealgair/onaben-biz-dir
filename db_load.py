#! /usr/bin/python
import sys, os
import time
import codecs
os.environ["PYTHONPATH"] = "/home/chase/Documents/Code/django/"
os.environ["DJANGO_SETTINGS_MODULE"] = "onaben.settings"
from directory.models import Business, Address, Category, Owner, PhoneNumber

dataDir = "/home/chase/Documents/Code/django/onaben/directory/data/NorthwestNativeABizDir/"
if len(sys.argv) > 1:
    dataDir = sys.argv[1]
if not dataDir.endswith("/"):
    dataDir = dataDir+"/"
modelFiles = {Business:"tblBizInfo.txt",
              Address:"tblBizAddyInfo.txt",
              Category:"tblBizCategories.txt",
              Owner:"tblBizOwnerInfo.txt",
              PhoneNumber:"tblBizPhoneNos.txt"}

metaData = {}
print("Meta Data:"  )
for line in open(dataDir+"columnheadings.txt"):
    if line.strip():
        tbl, cols = line.split(":")
        metaData[tbl.strip()] = [c.strip() for c in cols.split(",")]
        print '  ', tbl.strip()+":", metaData[tbl.strip()]
print

#e.g. 1/13/2007 0:00:00
fileDate = "%m/%d/%Y %H:%M:%S"
#YYYY-MM-DD
dbdate = "%Y-%m-%d"
epochdate = "1970-01-01"
def formatDate(date, default=None): #return null unless otherwise specified
    try:
        date = time.strptime(date, fileDate)
        date = time.strftime(dbdate, date)
        return date
    except ValueError:
        return default

def parseLine(line, delim = u","):
    line = line+u" "+delim    #last delim won't be returned
    fields = []
    field = u""
    inQuotes = False
    for char in line:
        if char == '"':
            inQuotes = not inQuotes
        elif not inQuotes and char == delim:
            yield field.strip()
            field = u""
        else:
            field += char

def parseFile(fileName, enc = 'iso-8859-1'):
    print("Parsing File %s..." % fileName)
    for line in codecs.open(dataDir+fileName, 'r', enc):
        #fields = parseLine(line, metaData[fileName.rstrip('.txt')])
        fields = dict(zip(metaData[fileName.rstrip('.txt')], parseLine(line)))
        print "  -----%s-----" % fileName
        for name, val in fields.iteritems():
            pval = val.encode('utf-8')
            print "    "+name+":", pval
        yield fields
    print("finished parsing")
    print

"tblBizInfo: NativeBizID, BusinessName, ContactFirstname, ContactLastname, ContactTitle, OwnershipTypeID, NW Region, BizWebsite, EmailAddress, Business description, StateDate, End Date, Home Based, FTE, PTE, Woman, Minority, SIC or Certification Type, E-mail List, Mailing List, Contact Me for Marketing Opps, ReferredBy, StillOperating, WillPublish, WillAdvertise, Date Registered, Last Updated, ReadytoPrint, Publish Online, OtherNotes"
for fields in parseFile("tblBizInfo.txt"):
    biz = Business(id = fields["NativeBizID"],
                   name = fields["BusinessName"],
                   nw_region = fields["NW Region"],
                   website = fields["BizWebsite"],
                   email = fields["EmailAddress"],
                   description = fields["Business description"],
                   start_date = formatDate(fields["StateDate"], epochdate),
                   end_date = formatDate(fields["End Date"]),
                   home_based = int(fields["Home Based"]),
                   full_time_employees = fields["FTE"],
                   part_time_employees = fields["PTE"],
                   woman = int(fields["Woman"]),
                   minority = int(fields["Minority"]),
                   sic_or_cert_type = fields["SIC or Certification Type"],
                   email_list = int(fields["E-mail List"]),
                   mailing_list = int(fields["Mailing List"]),
                   contact_for_marketing = int(fields["Contact Me for Marketing Opps"]),
                   referred_by = fields["ReferredBy"],
                   still_operating = int(fields["StillOperating"]),
                   will_publish = int(fields["WillPublish"]),
                   will_advertise = int(fields["WillAdvertise"]),
                   date_registered = formatDate(fields["Date Registered"], epochdate),
                   last_updated = formatDate(fields["Last Updated"]),
                   ready_to_print = int(fields["ReadytoPrint"]),
                   publish_online = int(fields["Publish Online"]),
                   other_notes = fields["OtherNotes"],
                   moderation = "Approved")
    biz.save()

"tblBizCategories: CategoryID, Business Category"
for fields in parseFile("tblBizCategories.txt"):
    cat = Category(id = fields["CategoryID"],
                   name = fields["Business Category"])
    cat.save()

"tblBiz-CategoryLink: NativeBizID, CategoryID"
for fields in parseFile("tblBiz-CategoryLink.txt"):
    if (fields["CategoryID"] and fields["NativeBizID"]):
        biz = Business.objects.get(id=fields["NativeBizID"])
        biz.categories.add(Category.objects.get(id=fields["CategoryID"]))
        biz.save

"tblBizAddyInfo:  NativeBizID, txtAddress, txtCity, txtState, txtZipCode, txtCountryOutsideUS, txtAddyType, DoNotPublishAddy"
for fields in parseFile("tblBizAddyInfo.txt"):
    addy = Address(business = Business.objects.get(id=fields["NativeBizID"]),
                   street = fields["txtAddress"],
                   city = fields["txtCity"],
                   state = fields["txtState"],
                   zipcode = fields["txtZipCode"],
                   country_outside_us = fields["txtCountryOutsideUS"],
                   addy_type = fields["txtAddyType"],
                   do_not_publish_addy = int(fields["DoNotPublishAddy"]))
    addy.save()

"tblBizOwnerInfo: Owner ID, Tribe, First Name, Last Name, Title, ONABEN Client"
for fields in parseFile("tblBizOwnerInfo.txt"):
    if fields["First Name"] and fields["Last Name"]:
        owner = Owner(id = fields["Owner ID"],
                      tribe = int(fields["Tribe"]),
                      first_name = fields["First Name"],
                      last_name = fields["Last Name"],
                      title = fields["Title"],
                      onaben_client = int(fields["ONABEN Client"]))
        owner.save()
    
"tblBiz-OwnerLink: BizOwnerLinkID, NativeBizID, BizOwnerID, Active, StartDate, EndDate, NotesHistory"
for fields in parseFile("tblBiz-OwnerLink.txt"):
    if fields["BizOwnerID"] and fields["NativeBizID"]:
        try:
            biz = Business.objects.get(id=fields["NativeBizID"])
            owner = Owner.objects.get(id=fields["BizOwnerID"])
            owner.business = biz
            owner.save()
        except:
            pass #not all owners will necessarily exist

"tblBizPhoneNos: NativeBizID, PhoneType, PhoneNumber, Extension"
for fields in parseFile("tblBizPhoneNos.txt"):
    phone = PhoneNumber(business = Business.objects.get(id=fields["NativeBizID"]),
                        phone_type = fields["PhoneType"],
                        phone_number = fields["PhoneNumber"],
                        extension = fields["Extension"])
    phone.save()





