# -*- coding: utf-8 -*-

#IMPORTS HERE
from __future__ import unicode_literals
import os
from . import country_list
from model_validators import *
from django.db import models
from django.utils.encoding import smart_unicode

from storage import OverwriteStorage
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#from django.contrib.auth.models import BaseUserManager
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, send_mass_mail

from django.utils import timezone
from upload_file_path import *


from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save


def get_full_name(self):
    if not self.last_name and not self.first_name:
        response = self.email
    else:
        response = str(self.first_name) + ' ' + str(self.last_name)
    return response
User.add_to_class("__str__", get_full_name)




class Payments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE )
    PAYMENT_CHOICES = (
        ( 'paypal', 'paypal' ),
        ( 'deposit', 'deposit' ),
    )
    NULL_CHOICES = (
        (None, 'Select'),
        (False, 'Rejected'),
        (True, 'Approved'),
    )
    
    created = models.DateTimeField( auto_now_add=True, auto_now= False)
    payment_approved = models.NullBooleanField( null = True, default = None, verbose_name = 'Payment Approval', choices = NULL_CHOICES, blank = False )
    amount = models.DecimalField( null = False, blank = False, max_digits = 50, decimal_places = 2 )
    payment_type = models.CharField( max_length = 80, null = False, choices = PAYMENT_CHOICES )
    transaction_fee = models.DecimalField(null = True, blank = True, max_digits = 50, decimal_places = 2 )
    proof = models.FileField( 
        #validators =[max_file_size(20000000), valid_file_extenions(['jpg','pdf'])],
        validators =[max_20BMfile_size, valid_extensions],
        null= False, blank=False, upload_to =payment_proof_upload_path, 
        )
        #help_text = "( MAX: 20MB ) You may attach a quote file with quote price, this file will be sent via email and show up in the client console.")
    #currency = models.CharField( max_length = 80, null=False, choices = PAYMENT_CHOICES )
    tax = models.DecimalField( max_digits= 50, null=True, blank = False, decimal_places=2, validators=[validate_positive_num], max_length = 1000 )
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def save(self, *args, **kwargs):
        try:
            new_image = self.proof
            #THROW EXCEPTION IF NO CURRENT IMAGE( max_length = 80, null = False, choices = PAYMENT_CHOICES )
            current_image = Payments.objects.get(id=self.id).proof
            if current_image != new_image:
                #this.profile_picture.delete(save=False)
                default_storage.delete(current_image.path)
        except: 
            pass # when new photo then we do nothing, normal case

        now = timezone.now()
        if self.payment_approved == True:
            self.services_set.all().update(solution_date = now)
        super(Payments, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        try:
            default_storage.delete(self.proof.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(Payments, self).delete(*args, **kwargs)



#ABSTRACT MODELS
class Services(models.Model):
    SERVICE_STATUS_CHOICES = (
        ( 'Pending Quote', 'Pending Quote' ),
        ( 'Quote Pending Client Approval', 'Quote Pending Client Approval' ),
        ( 'Pending Payment', 'Pending Payment' ),
        ( 'Pending Hecms Approval', 'Pending Hecms Approval' ),
        ( 'Payed', 'Payed' ),
        ( 'Resolved', 'Resolved' ),
    )


    payment = models.ForeignKey( Payments, null = True, on_delete= models.SET_NULL)
    quote_file = models.FileField( 
        #validators =[max_file_size(20000000), valid_file_extenions(['jpg','pdf'])],
        validators =[max_20BMfile_size, valid_extensions],
        null= True, blank=True, upload_to =quote_upload_path, 
        help_text = "( MAX: 20MB ) You may attach a quote file with quote price, this file will be sent via email and show up in the client console.",max_length = 1000)
    user = models.ForeignKey(User)
    created = models.DateTimeField( auto_now_add=True, auto_now= False )
    solution_date = models.DateTimeField( null = True )
    last_modified_ts = models.DateTimeField( auto_now=True, auto_now_add=False )
    quote_price = models.DecimalField(help_text = "Once you fill quote price, AND SAVE, client will be notified via email and the status will be changed to 'Quote Pending Client Approval'", max_digits= 50, null=True, blank = False, decimal_places=2, validators=[validate_positive_num])
    resolved = models.BooleanField(default= False, null = False)
    status = models.CharField(max_length = 50 ,null = False, blank = False, default = 'Pending Quote', choices = SERVICE_STATUS_CHOICES )
    quote_approved = models.NullBooleanField( null = True, default = None, verbose_name = 'Client Approval' )
    quote_payed = models.BooleanField(default = False)
    auction_products = models.ManyToManyField('Auction_Products', help_text = 'Lot Number')
    service_type = models.CharField(null = False, max_length = 20)
    has_open_process = models.BooleanField(default = False)
    report =models.FileField(null = True, blank = True, upload_to= report_upload_path, help_text="This can only be filled when the payment has been received (Only PDF accepted)", max_length = 1000)
    # class Meta:
    #     abstract = True
    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'

    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.id )

    def save(self, *args, **kwargs):
        if self.quote_approved and self.has_open_process and not self.quote_payed and self.quote_price:
            self.status = 'Pending Payment'
        if self.resolved:
            self.status = 'Resolved'
        super(Services, self).save(*args, **kwargs)





#USERAPP MODELS
class Auctions(models.Model):
    title = models.CharField( max_length = 80, null=False )
    created = models.DateTimeField(auto_now_add=True, auto_now= False)  
    host =   models.CharField( max_length = 80, null=False, blank = False )
    auction_begin = models.DateField()
    auction_end = models.DateField()
    address = models.CharField( max_length = 250, null = False, blank = False  )
    city = models.CharField(  max_length = 80, null=False, blank = False  )
    state_providence = models.CharField( max_length = 80, null=False, blank = False  ) 
    country = models.CharField( choices = country_list.value, max_length = 80, null=False, blank = False )
    zip_code = models.CharField( max_length = 10, null=True, blank = True)
    auction_open = models.BooleanField( default = True )
    users = models.ManyToManyField(User, through='Auction_Products')
    image=models.ImageField(upload_to = auction_image, blank = False, verbose_name = 'Auction Image', max_length = 1000)
    url = models.URLField(null  = False, blank= False)
    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'

    def save(self, *args, **kwargs):
        items = Auctions.objects.all()
        try:
            new_image = self.image
            #THROW EXCEPTION IF NO CURRENT IMAGE
            current_image = Auctions.objects.get(id=self.id).image
            if current_image != new_image:
                #this.profile_picture.delete(save=False)
                default_storage.delete(current_image.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(Auctions, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        try:
            default_storage.delete(self.image.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(Auctions, self).delete(*args, **kwargs)


    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.host + ' / ' + self.city +  ' / ' +str(self.auction_begin) )



class Auction_Products(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    #auction = models.ForeignKey(User, on_delete = models.CASCADE)
    item_name = models.CharField(max_length = 80, null=False )
    auction = models.ForeignKey('Auctions', on_delete = models.CASCADE )
    lot_number = models.CharField( max_length = 80, null=False, unique = True )
    image1 = models.ImageField(max_length = 1000, upload_to = auction_products, null = False, blank = False, verbose_name = 'Product Image')
    description = models.CharField(max_length = 250, null = False)
    # logistics = models.ForeignKey( 'Logistics', null = True, related_name = "products", on_delete = models.SET_NULL)
    # maintenance = models.ForeignKey( 'Maintenance', null = True, related_name = "maintenance_products", on_delete = models.SET_NULL)
    #has_open_process = models.BooleanField( default = False )
    created = models.DateTimeField(auto_now_add=True, auto_now= False)

    class Meta:
        verbose_name = 'Auction Product'
        verbose_name_plural = 'Auction Products'


    def save(self, *args, **kwargs):
        try:
            new_image = self.image1
            current_image = Auction_Products.objects.get(id=self.id).image1
            if current_image != new_image:
                # this.image1.delete(save=False)
                default_storage.delete(current_image.path)

        except: 
            pass # when new photo then we do nothing, normal case          
        super(Auction_Products, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        #super(Auction_Products, self).delete(*args, **kwargs)
        #LET THE USER KNOW THAT THE SERVICE HAS BEEN CANCELLED
        #  GO by EACH FIELD AND CHECK IF THERE IS A RELATED MODEL
        # if self.maintenance:
        #     self.maintenance.delete()

        # if self.logistics:
        #     logistics_related_producs =  self.logistics.products.exclude(id = self.id).exists()
        #     if not logistics_related_producs:
        #         self.logistics.delete()
        try:
            default_storage.delete(self.image1.path)
        except: 
            pass # when new photo then we do nothing, normal case
        # subject = 'Your request has been cancelled'
        # message = "We're sorry, your request service has been cancelled. You can request another quote by accessing your account"
        # sender= settings.DEFAULT_FROM_EMAIL
        # recipient = [self.user.email]
        # send_mail(subject, message, sender, recipient)
        super(Auction_Products, self).delete(*args, **kwargs)

    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.lot_number )

class Bank_Accounts(models.Model):
    bank = models.CharField(max_length = 25, null = True, blank = True)
    account_number = models.CharField(null = False, blank = False, max_length = 17, validators = [Integer_Only])
    aba_number = models.CharField(null = False, blank = False, max_length = 9)
    routing_number = models.CharField(null = False, blank = False,max_length = 9)
    details = models.TextField( max_length = 500 )
    address = models.CharField(max_length = 25, null = False, blank = False)
    city = models.CharField(max_length = 25, null = False, blank = False)
    state_providence = models.CharField(max_length = 25, null = False, blank = False)
    zip_code = models.IntegerField(null = True, blank = True)
    country =  models.CharField(max_length = 25, null = False, blank = False, choices = country_list.value)
    swift_number = models.CharField(null = True, max_length = 11, blank = True, validators=[min_length8])
    class Meta:
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'

    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.products.filter(logistics =self.id).first().user
        #return smart_unicode( user_instance.email )+ ' ' + '( %s )' %(get_full_name(user_instance) or 'No name established')
        return smart_unicode( self.bank )



class Logistics(models.Model):

    #user = models.ForeignKey(User)
    #auction_products = models.ForeignKey('Auction_Products')
    #lot_number = models.CharField( max_length = 80, null=False )
    service = models.OneToOneField('Services', on_delete = models.CASCADE, null = False)
    destination_lat = models.CharField(max_length = 25, null = True, blank = True)
    destination_lon = models.CharField(max_length = 25, null = True, blank = True)
    origin_lat = models.CharField(max_length = 25, null = True, blank = True)
    origin_lon = models.CharField(max_length = 25, null = True, blank = True)
    description = models.TextField( max_length = 500 )
    origin = models.TextField( null = False, blank = False )
    destination  = models.TextField(null = False, blank = False )
    class Meta:
        verbose_name = 'Logistics'
        verbose_name_plural = 'Logistics'

    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.products.filter(logistics =self.id).first().user
        #return smart_unicode( user_instance.email )+ ' ' + '( %s )' %(get_full_name(user_instance) or 'No name established')
        return smart_unicode( self.id )

# class Shipping(models.Model):
#     user = models.ForeignKey(User)
#     auction = models.ForeignKey('Auctions', on_delete = models.CASCADE )
#     #lot_number = models.CharField( max_length = 80, null=False )
#     created = models.DateTimeField(auto_now_add=True, auto_now= False)
#     description = models.TextField( max_length = 500 )
#     #origin
#     #destination
#     class Meta:
#         verbose_name = 'Shipping'
#         verbose_name_plural = 'Shipping'

#     def __unicode__( self ): #__str__ for python 3.3
#         return smart_unicode( self.auction )

class Maintenance(models.Model):
    CHOICES = (
        ( 'Client', 'Client' ),
        ( 'Hecms', 'Hecms' ),
    )
    service = models.OneToOneField('Services', on_delete = models.CASCADE, null = False)
    maintenance_type = models.CharField(max_length = 25, null = False )
    description = models.TextField( max_length = 500 )
    location = models.CharField( max_length = 80, null=False )
    parts_provider = models.CharField(max_length = 100, null = False, choices = CHOICES )

    class Meta:
        verbose_name = 'Maintenance'
        verbose_name_plural = 'Maintenance'

    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( self.id )



class Inspection_Types(models.Model):
    name = models.CharField( max_length = 80, null=False, blank = False )
    created = models.DateTimeField(auto_now_add=True, auto_now= False)
    price = models.DecimalField(null = False, blank = False, max_digits = 50, decimal_places = 2)
    description = models.TextField( max_length = 500 )
    section = models.ManyToManyField( 'Inspection_Types_Sections', verbose_name = 'Section', help_text = 'Add/Select' )
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Last Changed')
    class Meta:
        verbose_name = 'Inspection Types'
        verbose_name_plural = 'Inspection Types'
    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( self.name )


#SECTIONS IN AN INSPECTION REPORT TEMPLATE
class Inspection_Types_Sections(models.Model):
    name = models.CharField( max_length = 80, null=False, blank = False )
    created = models.DateTimeField(auto_now_add=True, auto_now = False)
    # price = models.DecimalField(null = False, blank = False, max_digits = 50, decimal_places = 2)
    #description = models.TextField( max_length = 500, null = True, blank = True )
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Last Changed')
    class Meta:
        verbose_name = 'Inspection Types Section'
        verbose_name_plural = 'Inspection Types Sections'
    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( self.name )


#INSPECTION REPORT ITEMS IN A TEMPLATE SECTION
class Inspection_Types_Sections_Items(models.Model):
    section = models.ForeignKey( Inspection_Types_Sections, null = True, blank = True )

    created = models.DateTimeField(auto_now_add=True, auto_now = False)
    description = models.CharField( max_length = 80, null=False, blank = False )
    #rating = models.IntegerField(null = False, default = 0, blank =  True )
    #details = models.TextField( max_length = 500, null = True, blank = True )
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name = 'Last Changed')
    #item_picture = models.ImageField( upload_to = upload_profile_picture, null = True, blank = True )#storage=OverwriteStorage(), 

    class Meta:
        verbose_name = 'Inspection Type Section Item'
        verbose_name_plural = 'Inspection Type Section Items'
    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( self.description )


class Inspection_Reports( models.Model ):
    created = models.DateTimeField( auto_now_add=True, auto_now= False )
    inspection = models.OneToOneField( 'Inspections', null = True, blank = True )
    class Meta:
        verbose_name = 'Inspection Report'
        verbose_name_plural = 'Inspection Reports'

    def delete(self, *args, **kwargs):
        #DELETE IMAGERY ON DELETE
        rows = self.inspection_report_rows_set.all()
        for row in rows:
            try:
                default_storage.delete(self.row.item_picture.path )
            except:
                pass

        super(Inspection_Reports, self).delete(*args, **kwargs)


#ROW IN A REPORTTHAT IS RELATED TO ITEMS AND TO A REPORT
class Inspection_Report_Rows( models.Model ):
    created = models.DateTimeField( auto_now_add =True, auto_now = False )
    inspection_report = models.ForeignKey( Inspection_Reports, null = True, on_delete = models.CASCADE )
    row = models.ForeignKey( Inspection_Types_Sections_Items, on_delete = models.CASCADE )
    rating = models.IntegerField(null = True, default = 0, blank =  True )
    details = models.CharField( max_length = 500, null = True, blank = True )
    item_picture = models.ImageField( max_length = 1000,upload_to = inspection_item_picture, null = True, blank = True )#storage=OverwriteStorage(), 
    class Meta:
        verbose_name = 'Inspection Report Row'
        verbose_name_plural = 'Inspection Report Rows'

    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( self.id )

    def delete(self, *args, **kwargs):
        #default_storage.delete(self.item_picture.path)
        try:
            default_storage.delete(self.item_picture.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(Inspection_Report_Rows, self).delete(*args, **kwargs)



class Inspections( models.Model ):
    service = models.OneToOneField('Services', on_delete = models.CASCADE)
    description = models.TextField( max_length = 500 )
    inspection_type = models.ForeignKey('Inspection_Types', on_delete = models.PROTECT, null = True)

    class Meta:
        verbose_name = 'Inspection'
        verbose_name_plural = 'Inspections'

    def __unicode__( self ): #__str__ for python 3.3
        #user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( self.id )



########################################################################

# Create your models here.
def upload_landing(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'admin_content', 'index', 'landing', filename ))

class Landing_Page_Images(models.Model):
    TIPO_OPTIONS =  (
        ( 'IMAGEN1', 'IMAGEN1' ),
        ( 'IMAGEN2', 'IMAGEN2' ),
        ( 'IMAGEN3', 'IMAGEN3' ),
        ( 'IMAGEN4', 'IMAGEN4' ),
        ( 'IMAGEN5', 'IMAGEN5' ),
    )
    # condominio = models.ForeignKey('Condominio', null = True)
    title = models.CharField(max_length = 25, null = False, unique = True, choices = TIPO_OPTIONS)
    # descripcion = models.CharField(max_length = 500, null = True)
    image = models.ImageField(upload_to = upload_landing, null = False, blank = False, max_length = 1000)
    created = models.DateTimeField(auto_now_add=True, auto_now= False)
    # fecha_de_emision = models.DateTimeField(auto_now_add=True, null=True)
    def __unicode__(self): #__str__ for python 3.3
        return smart_unicode(self.title)

    class Meta:
        verbose_name = 'Landing Page Image'
        verbose_name_plural = 'Landing Page Images'

    def save(self, *args, **kwargs):
        try:
            new_image = self.image
            #THROW EXCEPTION IF NO CURRENT IMAGE
            current_image = Landing_Page_Images.objects.get(id=self.id).image
            if current_image != new_image:
                #this.profile_picture.delete(save=False)
                default_storage.delete(current_image.path)
        except: 
            pass # when new photo then we do nothing, normal case          
        super(Landing_Page_Images, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        try:
            default_storage.delete(self.image.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(Landing_Page_Images, self).delete(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # custom fields for user
    mobile_number = models.CharField(max_length=12, null  = True )
    office_number = models.CharField(max_length=12, null  = True )
    company_name = models.CharField( max_length=100, blank = True, null = True )
    profile_picture = models.ImageField( upload_to = upload_profile_picture, null = True, blank = True, max_length = 1000 )#storage=OverwriteStorage(), 
    

    def image_tag(self):
        return u'<img src="/media/%s" width="auto" height="100" alt="No Profile Pic"/>' % self.profile_picture
    #image_tag.short_description = 'Image'
    #image_tag.allow_tags = True
    def save(self, *args, **kwargs):
        try:
            new_image = self.profile_picture
            #THROW EXCEPTION IF NO CURRENT IMAGE
            current_image = UserProfile.objects.get(id=self.id).profile_picture
            if current_image != new_image:
                #this.profile_picture.delete(save=False)
                default_storage.delete(current_image.path)
        except: 
            pass # when new photo then we do nothing, normal case          
        super(UserProfile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        try:
            default_storage.delete(self.profile_picture.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(UserProfile, self).delete(*args, **kwargs)





#USERAPP MODELS

    # title = models.CharField( max_length = 80, null=False )
    # created = models.DateTimeField(auto_now_add=True, auto_now= False)  
    # host =   models.CharField( max_length = 80, null=False, blank = False )
    # auction_begin = models.DateField()
    # auction_end = models.DateField()
    # address = models.CharField( max_length = 250, null = False, blank = False  )
    # city = models.CharField(  max_length = 80, null=False, blank = False  )
    # state_providence = models.CharField( max_length = 80, null=False, blank = False  ) 
    # country = models.CharField( choices = country_list.value, max_length = 80, null=False, blank = False )
    # zip_code = models.CharField( max_length = 10, null=True, blank = True)
    # auction_open = models.BooleanField( default = True )
    # class Meta:
    #     verbose_name = 'Auction'
    #     verbose_name_plural = 'Auctions'

    # def __unicode__( self ): #__str__ for python 3.3
    #     return smart_unicode( self.host )

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):

    try:
    #if instance.userprofile:
        instance.userprofile.save()
    #else:
    except:
        userprofile = UserProfile.objects.create(user = instance)
        instance.userprofile = userprofile
        instance.userprofile.save()


class Carousel_Image(models.Model):
    ITEM_TYPE =  (
        ( 'Inspection', 'Inspection' ),
        ( 'Auction', 'Auction' ),
        ( 'Logistics', 'Logistics' ),
        ( 'Maintenance', 'Maintenance' ),
        ( 'Facebook', 'Facebook' ),
        ( 'Twitter', 'Twitter' ),
        ( 'Instagram', 'Instagram' ),
        ( 'Social Media', 'Social Media' ),
    )
    image = models.ImageField(upload_to = upload_landing, null = False, blank = False, max_length = 1000)
    created = models.DateTimeField( auto_now_add=True, auto_now= False)
    text = models.CharField( max_length = 25, null = True, blank = True)
    counter = models.IntegerField(null = True, blank = True)
    item_type = models.CharField( max_length = 25, null = True, blank = False, choices = ITEM_TYPE)
    origin = models.TextField(max_length = 500, blank = True, null= True )
    destination = models.TextField(max_length = 500, blank = True, null= True )
    maintenance_description = models.TextField(max_length = 500, blank = True, null= True )
    inspection_type = models.TextField(max_length = 500, blank = True, null= True )
    lot_number = models.CharField(max_length = 500, blank = True, null= True )
    price = models.CharField(max_length = 500, blank = True, null= True )
    date = models.CharField(max_length = 500, blank = True, null= True )
    url = models.CharField(max_length = 500, blank = True, null= True )
    service = models.OneToOneField(Services, null = True)
    def save(self, *args, **kwargs):
        items = Carousel_Image.objects.all()
        try:
            new_image = self.image
            #THROW EXCEPTION IF NO CURRENT IMAGE
            current_image = Carousel_Image.objects.get(id=self.id).image
            if current_image != new_image:
                #this.profile_picture.delete(save=False)
                default_storage.delete(current_image.path)
        except: 
            pass # when new photo then we do nothing, normal case
        self.counter = len(items) +1
        super(Carousel_Image, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):

        try:
            default_storage.delete(self.image.path)
        except: 
            pass # when new photo then we do nothing, normal case

        super(Carousel_Image, self).delete(*args, **kwargs)

    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.text )




class SampleCarouselServices(models.Model):
    CHOICES = (
        ( 'Inspections', 'Inspection' ),
        ( 'Logistics', 'Logistics' ),
        ( 'Maintenance', 'Maintenance' ),
    )
    unique_id = models.AutoField(null= False, blank = False, primary_key= True)
    object_type= models.CharField(choices=CHOICES,max_length = 500, blank = False, null= False )
    image = models.ImageField(null= False, blank = False)
    report = models.FileField(null = True, blank = True, upload_to= report_upload_path, help_text="Only for Maintenance and Logistics", max_length = 1000)
    sample = models.BooleanField(default = True, blank= True) 
    class Meta:
        verbose_name = 'Carousel Sample'
        verbose_name_plural = 'Carousel Samples'
    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.unique_id )

class SampleInspectionReportRow(models.Model):

    SECTIONS_CHOICES = (
        ( 'Chasis', 'Chasis' ),
        ( 'Hydraulics', 'Hydraulics' ),
        ( 'Drivetrain', 'Drivetrain' ),
        ( 'Engine', 'Engine' ),
        ( 'General Appearance', 'General Appearance' ),
        ( 'Control Station', 'Control Station' ),
    )

    details_choices = (
        ( 1, 1 ),
        ( 2, 2 ),
        ( 3, 3 ),
        ( 4, 4 ),
    )
    details = models.CharField( max_length = 250, null = False, blank = False,verbose_name='Inspected part Name', help_text='What part of are you inspecting?' )
    description = models.CharField(max_length = 250, null = False, blank = False )
    inspection = models.ForeignKey(SampleCarouselServices, null= False, verbose_name='Sample inspection ID', related_name='rows')
    rating = models.IntegerField(choices=details_choices,null = False, default = 0, blank =  False )
    image= models.ImageField(null= False, blank = False)
    section = models.CharField( max_length = 80, null = False, choices = SECTIONS_CHOICES )
