# -*- coding: utf-8 -*-

#IMPORTS HERE
from __future__ import unicode_literals
import os
from . import country_list
from model_validators import *
from django.db import models
from django.utils.encoding import smart_unicode
from django.db.models.signals import post_delete, post_save, pre_save
from storage import OverwriteStorage
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
#from django.contrib.auth.models import BaseUserManager
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, send_mass_mail

def get_full_name(self):
    return (str(self.first_name) + ' ' + str(self.last_name))
User.add_to_class("__str__", get_full_name)



def quote_upload_path(instance, filename):
    model_name = str(instance.__class__.__name__).lower()
    if model_name == 'logistics':
        user = instance.products.filter(logistics =instance.id).first().user
    elif model_name == 'maintenance':
        user = instance.maintenance_products.filter(maintenance =instance.id).first().user
    return os.path.join( '%s/%s/%s_quotes/%s' % ( 'user_files', str(user.pk), model_name, filename ))

#ABSTRACT MODELS
class ServiceStatus(models.Model):
    SERVICE_STATUS_CHOICES = (
        ( 'Pending Quote', 'Pending Quote' ),
        ( 'Quote Pending Client Approval', 'Quote Pending Client Approval' ),
        ( 'Quote Accepted by client', 'Quote Accepted by client' ),
        ( 'Resolved', 'Resolved' ),
    )


    quote_file = models.FileField( 
        #validators =[max_file_size(20000000), valid_file_extenions(['jpg','pdf'])],
        validators =[max_20BMfile_size, valid_extensions],
        null= True, blank=True, upload_to =quote_upload_path, 
        help_text = "( MAX: 20MB ) You may attach a quote file with quote price, this file will be sent via email and show up in the client console.")
    
    created = models.DateTimeField(auto_now_add=True, auto_now= False)
    solution_date = models.DateField(null = True)
    last_modified_ts = models.DateTimeField(auto_now=True, auto_now_add=False)
    quote_price = models.DecimalField(help_text = "Once you fill quote price, AND SAVE, client will be notified via email and the status will be changed to 'Quote Pending Client Approval'", max_digits= 50, null=True, blank = False, decimal_places=2, validators=[validate_positive_num])
    resolved = models.BooleanField(default= False, null = False)
    status = models.CharField(max_length = 50 ,null = False, blank = False, default = 'Pending Quote', choices = SERVICE_STATUS_CHOICES )
    quote_approved = models.NullBooleanField( null = True, default = None, verbose_name = 'Client Approval' )
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        model_name = self.__class__.__name__
        if model_name == 'Logistics':
            products = self.products.filter(logistics = self.id)
            for product in products:
                product.has_open_process = True
                product.save()

        elif model_name == 'Maintenance':
            product = self.maintenance_products.filter(maintenance = self.id).first().has_open_process = True
            product.save()
        super(ServiceStatus, self).save(*args, **kwargs)
        #print dir(self)
        #print self.auction_products
        # self.auction_products.has_open_process = True
        # print args, kwargs
    #     print parameter
    #     #email the user when status updates
    #     #determine if status has changed
    #     #print self.auction_products
    #     print args, kwargs
        # if not self.slug:
        #     slug = slugify(unicode(self.name).encode('trans'))
        # else:
        #     slug = self.slug
        # count = self.__class__.objects.filter(slug = slug).count()
        # if count > 1:
        #     if slug[-2]=='_':
        #         count = int(slug[-1])
        #         slug = slug[:-2]
        #     self.slug = '{0}_{1}'.format(slug,count+1)
        # else:
        #     self.slug = slug
        #super(ServiceStatus, self).save(*args, **kwargs)






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
    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'

    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.host )


def auction_products(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'user_files', str(instance.user.pk), 'auction_products', filename ))

class Auction_Products(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item_name = models.CharField(max_length = 80, null=False )
    auction = models.ForeignKey('Auctions')
    lot_number = models.CharField( max_length = 80, null=False, unique = True )
    image1 = models.ImageField(upload_to = auction_products, null = False, blank = False, verbose_name = 'Product Image 1')
    description = models.CharField(max_length = 250, null = False)
    logistics = models.ForeignKey( 'Logistics', null = True, related_name = "products", on_delete = models.SET_NULL)
    maintenance = models.ForeignKey( 'Maintenance', null = True, related_name = "maintenance_products", on_delete = models.SET_NULL)
    has_open_process = models.BooleanField( default = False )
    
    class Meta:
        verbose_name = 'Customer Products and Services'
        verbose_name_plural = 'Customer Products and Services'
    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.lot_number )

    def save(self, *args, **kwargs):
        try:
            this = Auction_Products.objects.get(id=self.id)
            if this.image1 != self.image1:
                this.image1.delete(save=False)
                default_storage.delete(self.__this.image1.path)
        except: 
            pass # when new photo then we do nothing, normal case          
        super(Auction_Products, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        #LET THE USER KNOW THAT THE SERVICE HAS BEEN CANCELLED
        #  GO THROUGH EACH FIELD AND CHECK IF THERE IS A RELATED MODEL
        if self.maintenance:
            self.maintenance.delete()

        if self.logistics:
            logistics_related_producs =  self.logistics.products.exclude(id = self.id).exists()
            if not logistics_related_producs:
                self.logistics.delete()
        try:
            default_storage.delete(self.image1.path)
        except: 
            pass # when new photo then we do nothing, normal case
        subject = 'Your request has been cancelled'
        message = "We're sorry, your request service has been cancelled. You can request another quote by accessing your account"
        sender= settings.DEFAULT_FROM_EMAIL
        recipient = [self.user.email]
        send_mail(subject, message, sender, recipient)
        super(Auction_Products, self).delete(*args, **kwargs)


class Logistics(ServiceStatus):

    #user = models.ForeignKey(User)
    #auction_products = models.ForeignKey('Auction_Products')
    #lot_number = models.CharField( max_length = 80, null=False )
    destination_lat = models.CharField(max_length = 25, null = True, blank = True)
    destination_lon = models.CharField(max_length = 25, null = True, blank = True)
    origin_lat = models.CharField(max_length = 25, null = True, blank = True)
    origin_lon = models.CharField(max_length = 25, null = True, blank = True)
    description = models.TextField( max_length = 500 )
    origin = models.TextField( )
    destination  = models.TextField( )
    class Meta:
        verbose_name = 'Logistics'
        verbose_name_plural = 'Logistics'

    def __unicode__( self ): #__str__ for python 3.3
        user_instance = self.products.filter(logistics =self.id).first().user
        return smart_unicode( user_instance.email )+ ' ' + '( %s )' %(get_full_name(user_instance) or 'No name established')
        #return smart_unicode( user_instance )

class Shipping(models.Model):
    user = models.ForeignKey(User)
    auction = models.ForeignKey('Auctions', on_delete = models.CASCADE )
    #lot_number = models.CharField( max_length = 80, null=False )
    created = models.DateTimeField(auto_now_add=True, auto_now= False)
    description = models.TextField( max_length = 500 )
    #origin
    #destination
    class Meta:
        verbose_name = 'Shipping'
        verbose_name_plural = 'Shipping'

    def __unicode__( self ): #__str__ for python 3.3
        return smart_unicode( self.auction )

class Maintenance(ServiceStatus):
    CHOICES = (
        ( 'Client', 'Client' ),
        ( 'Hecms', 'Hecms' ),
    )
    #user = models.ForeignKey(User)
    #auction = models.ForeignKey('Auctions', on_delete = models.CASCADE )
    #lot_number = models.CharField( max_length = 80, null=False )
    created = models.DateTimeField(auto_now_add=True, auto_now= False)
    description = models.TextField( max_length = 500 )
    location = models.CharField( max_length = 80, null=False )
    parts_provider = models.CharField(max_length = 100, null = False, choices = CHOICES )

    class Meta:
        verbose_name = 'Maintenance'
        verbose_name_plural = 'Maintenance'

    def __unicode__( self ): #__str__ for python 3.3
        user_instance = self.maintenance_products.get(maintenance = self.id).user
        return smart_unicode( user_instance.email )+ ' ' + '( %s )' %(get_full_name(user_instance) or 'No name established')

########################################################################

# Create your models here.
def upload_carousel(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'admin_content', 'index', 'carousel', filename ))

class Index_Page_Carousel(models.Model):
    # condominio = models.ForeignKey('Condominio', null = True)
    title = models.CharField(max_length = 25, null = False)
    # descripcion = models.CharField(max_length = 500, null = True)
    image = models.ImageField(upload_to = upload_carousel, null = False, blank = False)
    created = models.DateTimeField(auto_now_add=True, auto_now= False)
    # fecha_de_emision = models.DateTimeField(auto_now_add=True, null=True)
    def __unicode__(self): #__str__ for python 3.3
        return smart_unicode(self.title)

    class Meta:
        verbose_name = 'Carousel Image'
        verbose_name_plural = 'Carousel Images'


def upload_profile_picture(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'user_files', str(instance.user.pk), 'profile_picture', filename ))

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # custom fields for user
    company_name = models.CharField( max_length=100, blank = True, null = True )
    profile_picture = models.ImageField( upload_to = upload_profile_picture, null = True, blank = True )#storage=OverwriteStorage(), 
    

    #image = ImageField(...) # works with FileField also
    def save(self, *args, **kwargs):
        try:
            this = UserProfile.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture:
                this.profile_picture.delete(save=False)
                default_storage.delete(self.__this.profile_picture.path)
        except: 
            pass # when new photo then we do nothing, normal case          
        super(UserProfile, self).save(*args, **kwargs)


#USERAPP MODELS
class Service(models.Model):
    
    pass
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
