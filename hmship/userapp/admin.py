# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from .models import *
from django.utils.encoding import smart_unicode
from django.contrib import messages
from django.shortcuts import render
#USED TO GET URL
from django.contrib.sites.models import Site
#from django.contrib.auth.models import User
from django.utils.html import format_html
from userapp.forms import CarouselItemsForm, Inspection_ReportForm, SampleReportForm
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
admin.site.site_title = 'Hecms Administrator'
admin.site.site_header = 'Hecms Administrator'
admin.site.index_title = 'Control Panel'
admin.site.site_url = '/'


# Register your models here.
# class Carousel_content_Admin(admin.ModelAdmin):
# 	pass
#     # search_fields = ['=id', 'condominio__rif', ]
#     # list_filter = ('timestamp', 'fechafacturacion',)  
#     # save_on_top = True
#     # form = Egresos_Condominio_Form
#     # fields = [  'monto', 'fechafacturacion', 'detalle', 'publicado']
#     #list_display =['user', 'sms_balance', 'active', 'timestamp']
# admin.site.register(Index_Page_Carousel, Carousel_content_Admin)

# class UserAdmin( admin.ModelAdmin ):
#     pass
# admin.site.register( User, UserAdmin )


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'





class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ['id', 'username', 'first_name', 'last_name','company_name','email', 'mobile_number','office_number','is_staff', 'is_superuser', 'is_active', 'profile_picture']
    list_editable = ('is_active', )
    search_fields = ['id', 'email', 'first_name', 'last_name' ]
    list_filter = ('is_active', 'is_superuser', 'is_staff',)  
    readonly_fields = ('mobile_number','office_number', 'company_name','profile_picture')
    def mobile_number(self, obj):
        return obj.userprofile.mobile_number
    def office_number(self, obj):
        return obj.userprofile.office_number 
    def company_name(self, obj):
        return obj.userprofile.company_name
    def profile_picture(self, obj):
        return mark_safe(obj.userprofile.image_tag())
        # html = u' <img src="%s" />' %(obj.userprofile.profile_picture)admin_thumbnail
        # print obj.userprofile.profile_picture
        # return mark_safe(html)
    #profile_picture.allow_tags = True
    # def image_tag(self):
    #     return u'<img src="%s" />' % <URL to the image>          
    #mobile_number.allow_tags = True
    mobile_number.short_description = "Mobile"
    office_number.short_description = "Office #"
    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class Landing_Page_ImagesAdmin(admin.ModelAdmin ):
    list_display = ['title', 'created', 'image' ]
admin.site.register(Landing_Page_Images, Landing_Page_ImagesAdmin)


class UserProfileAdmin( admin.ModelAdmin ):
    def user_instance(self, obj):
        return 'Id: '+ str(obj.user.pk)  + ' - ' + str(obj.user.first_name) + ' ' + str(obj.user.last_name)
    def first_name(self, obj):
        return smart_unicode(obj.user.first_name)
    def last_name(self, obj):
        return smart_unicode(obj.user.last_name)
    #user_instance.short_description = 'user_instance'
    # search_fields = ['=id', 'condominio__rif', ]
    # list_filter = ('timestamp', 'fechafacturacion',)  
    # save_on_top = True
    # form = Egresos_Condominio_Form
    readonly_fields = ('user_instance', 'first_name', 'last_name', 'mobile_number', 'office_number', 'profile_picture', 'company_name',)
    fields = [ 'user_instance', 'first_name', 'last_name','company_name',  'profile_picture', 'mobile_number', 'office_number' ]
    list_display = ['id', 'first_name', 'last_name', 'company_name', 'profile_picture' ]
admin.site.register( UserProfile, UserProfileAdmin )

# Register your models here.


class Logistics_Admin(admin.ModelAdmin):
    # search_fields = ['=id', 'condominio__rif', ]
    # list_filter = ('timestamp', 'fechafacturacion',)  
    # save_on_top = True
    # form = Egresos_Condominio_Form
    
    
    def origin_g(self, obj):
        if obj.origin_lon  and obj.origin_lat:
            url = 'https://www.google.com/maps/@%s,%s,16z' %(obj.origin_lat , obj.origin_lon )
            html ='<span>%s</span><a style="margin-left:10px;" href="%s"><b>%s</b></a>' % (obj.origin, url, 'View in Google Maps')
            return html
        else:
            return obj.origin   
        return 'Not Avaliable'
    origin_g.allow_tags = True
    origin_g.short_description = "Origin"

    def destination_g(self, obj):
        if obj.destination_lon  and obj.destination_lat:
            url = 'https://www.google.com/maps/@%s,%s,16z' %(obj.destination_lat , obj.destination_lon )
            html ='<span>%s</span><a style="margin-left:10px;" href="%s"><b>%s</b></a>' % (obj.destination, url, 'View in Google Maps')
            return html
        else:
            return obj.origin
        return 'Not Avaliable'
    destination_g.allow_tags = True
    destination_g.short_description = "Destination"

    # def user_instance(self, obj):
    #     return obj

    # def approval_status(self, obj):
    #     approval = obj.quote_approved
    #     if not approval:
    #         approval = 'Not revised by Client'
    #     return approval

    # def user_name(self, obj):
    #     return obj


    # def quote_price(self, obj):
    #     return obj.service.quote_price



    fields = [
        #'id',
        #'service__quote_price',
        #'service__approval_status',
        #'service__quote_file',
        #'service__resolved',
        #'created',
        'origin_g',
        'destination_g',
        'description',
        #'service__solution_date',
        #'service__quote_approved'
    ]
    readonly_fields = (
        # 'user_instance',
        # 'created',
        # 'description',
        'origin_g',
        'destination_g',
        # 'solution_date',
        # 'status',
        # 'resolved',
        # 'approval_status',
        # 'quote_file',
        # 'quote_approved', 
    )
    list_display = [ 'id', 'origin', 'destination', 'description']
    #list_display = [ 'service', 'status', 'quote_price', 'approval_status', 'quote_file', 'resolved', 'user_instance','created', 'origin_g', 'destination_g', 'description', 'solution_date','quote_approved']


    #save method
    #def save_model(self, request, obj, form, change):
        # GET USER
        # client = obj.products.filter(logistics =obj.id).first().user
        # if obj.quote_price and form.has_changed():
        #     if 'quote_price' in form.changed_data and not form.initial['quote_price']:
        #         obj.status = 'Quote Pending Client Approval'
        #         email = EmailMessage(
        #             'You have a new logistics quote!',
        #             'Dear %s, you have a logistics quote pending your review'
        #             '. Please read the information carefully in your account or if this message includes an attachment. You may login to your' 
        #             ' account at any time to reply to such quote.' %(client.get_full_name().title() or client),
        #             settings.DEFAULT_FROM_EMAIL,
        #             [client.email],
        #             #['bcc@example.com'],
        #             reply_to=[settings.LOGISTICS_EMAIL],
        #             #headers={'Message-ID': 'foo'},
        #         )

        #         if obj.quote_file:
        #             file = request.FILES.get('quote_file')
        #             content_type = str(file.content_type)
        #             file_name = str(file.name)
        #             # attachment = open(file, 'rb')
        #             email.attach(file_name, file.read(), content_type)
        #         #send an email to user notifying that a quote was created
        #         email.send()

        #     elif 'quote_file' in form.changed_data and obj.quote_file and not form.initial['quote_file']:
        #         email = EmailMessage(
        #             'You have a new logistics quote!',
        #             'Dear %s, you have a logistics quote pending your review'
        #             '. Please read the information carefully in your account or if this message includes an attachment. You may login to your' 
        #             ' account at any time to reply to such quote.' %(client.get_full_name().title() or client),
        #             settings.DEFAULT_FROM_EMAIL,
        #             [client.email],
        #             #['bcc@example.com'],
        #             reply_to=[settings.LOGISTICS_EMAIL],
        #             #headers={'Message-ID': 'foo'},
        #         )

        #         if obj.quote_file:
        #             file = request.FILES.get('quote_file')
        #             content_type = str(file.content_type)
        #             file_name = str(file.name)
        #             # attachment = open(file, 'rb')
        #             email.attach(file_name, file.read(), content_type)

        #super(Logistics_Admin, self).save_model(request, obj, form, change)
admin.site.register(Logistics, Logistics_Admin)


#default_related_name, related_objects,related_fkey_lookups


class Maintenance_Admin(admin.ModelAdmin):
    # search_fields = ['=id', 'condominio__rif', ]
    # list_filter = ('timestamp', 'fechafacturacion',)  
    # save_on_top = True
    # form = Egresos_Condominio_Form
    # def location_g(self, obj):
    #     lat = str(10.500000)
    #     lon = str(-66.916664)
    #     if lon and lat:
    #         url = 'https://www.google.com/maps/@%s,%s,10z' %(lat, lon)
    #         html ='<span>%s</span><a style="margin-left:10px;" href="%s"><b>%s</b></a>' % (obj.location, url, 'View in Google Maps')
    #         return html
    #     return 'Not Avaliable'
    # location_g.allow_tags = True
    # location_g.short_description = "Location"

    # def user_instance(self, obj):
    #     return obj
    #fields = [ 'created', 'origin', 'destination', 'description']
    fields = [ 'service' ,'location', 'parts_provider','description']
    readonly_fields = ('parts_provider', 'description', 'location', 'service',)
    list_display  = [ 'service' ,'location', 'parts_provider','description']
admin.site.register(Maintenance, Maintenance_Admin)


class Payments_Admin(admin.ModelAdmin):
    # search_fields = ['=id', 'condominio__rif', ]
    # list_filter = ('timestamp', 'fechafacturacion',)  
    # save_on_top = True
    # form = Egresos_Condominio_Form
    def approve_payment(self, obj):
        if obj.payment_type == 'deposit':
            #html ='<select>%s</select><a style="margin-left:10px;" href="%s"><b>%s</b></a>' % (obj.location, url, 'View in Google Maps')
            return obj.payment_approved
        else:
            return 'Does not apply'

    def proof_obj(self, obj):
        if obj.payment_type == 'deposit':
            #html ='<select>%s</select><a style="margin-left:10px;" href="%s"><b>%s</b></a>' % (obj.location, url, 'View in Google Maps')
            return obj.proof

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.payment_approved == True or obj.payment_approved == False:
                return self.readonly_fields + ('payment_approved',)
                # if obj.quote_file:
                #     return self.readonly_fields + ('quote_price',) + ('quote_file',)
                # return self.readonly_fields + ('quote_price',) 
        return self.readonly_fields
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     # instance = Services.objects.get(id = object_id)

    #     # if instance.service_type =='Logistics':
    #     #     self.inlines = (LogisticsInline, )
    #     # elif instance.service_type =='Maintenance':
    #     #     self.inlines = (MaintenanceInline, )
    #     # elif instance.service_type =='Inspection':
    #     #     self.inlines = (InspectionsInline, )

    #     return super(Payments_Admin, self).change_view(request, object_id)

    def save_model(self, request, obj, form, change):
        client = obj.user
        payment_status = 'Accepted' if obj.payment_approved ==True else 'Rejected'

        if form.has_changed() and obj.payment_approved:

            for service in obj.services_set.all():
                #service.resolved = True
                service.status = 'Payed'
                service.quote_payed = True
                service.save()

        # obj.service.status = 'Resolved'
        # obj.service.quote_payed = True if obj.payment_approved == True else False
        # obj.service.save()
        email = EmailMessage(
            'Your payment has been %s!' %(payment_status),
            'Dear %s, your payment has been %s'
            '. For updates on your order ( if approved ) feel free to check your Hecms account Order Book. You will also be notified via email' %( client.get_full_name().title() or client, payment_status),
            settings.DEFAULT_FROM_EMAIL,
            [client.email],
            #['bcc@example.com'],
            reply_to=[settings.LOGISTICS_EMAIL],
            #headers={'Message-ID': 'foo'},
        )
        email.send()
        # # GET USER
        # client = obj.user
        # if obj.quote_price and form.has_changed():
        #     if 'quote_price' in form.changed_data and not form.initial['quote_price']:
        #         obj.status = 'Quote Pending Client Approval'
        #         obj.has_open_process = True
        #         if obj.quote_file:
        #             quote_origin = 'attachment'
        #         else:
        #             quote_origin = 'account'
        #         email = EmailMessage(
        #             'You have a new %s quote!' %(obj.service_type),
        #             'Dear %s, you have a logistics quote pending your review'
        #             '. Please read the information carefully in your %s. You may login to your' 
        #             ' account at any time to reply to such quote.' %(client.get_full_name().title() or client, quote_origin),
        #             settings.DEFAULT_FROM_EMAIL,
        #             [client.email],
        #             #['bcc@example.com'],
        #             reply_to=[settings.LOGISTICS_EMAIL],
        #             #headers={'Message-ID': 'foo'},
        #         )

        #         if obj.quote_file:
        #             file = request.FILES.get('quote_file')
        #             content_type = str(file.content_type)
        #             file_name = str(file.name)
        #             # attachment = open(file, 'rb')
        #             email.attach(file_name, file.read(), content_type)
        #         #send an email to user notifying that a quote was created
        #         email.send()

        #     elif 'quote_file' in form.changed_data and obj.quote_file and not form.initial['quote_file']:
        #         email = EmailMessage(
        #             'You have a new logistics quote!',
        #             'Dear %s, you have a logistics quote pending your review'
        #             '. Please read the information carefully in your account or if this message includes an attachment. You may login to your' 
        #             ' account at any time to reply to such quote.' %(client.get_full_name().title() or client),
        #             settings.DEFAULT_FROM_EMAIL,
        #             [client.email],
        #             #['bcc@example.com'],
        #             reply_to=[settings.LOGISTICS_EMAIL],
        #             #headers={'Message-ID': 'foo'},
        #         )

        #         if obj.quote_file:
        #             file = request.FILES.get('quote_file')
        #             content_type = str(file.content_type)
        #             file_name = str(file.name)
        #             # attachment = open(file, 'rb')
        #             email.attach(file_name, file.read(), content_type)
        #         email.send()
        super(Payments_Admin, self).save_model(request, obj, form, change)

    fields = [ 'user' ,'amount', 'tax','transaction_fee','created','payment_type', 'payment_approved', 'proof' ]
    readonly_fields = ('user', 'amount', 'tax','payment_type','created', 'transaction_fee', 'proof',)
    list_display  = [ 'id' ,'amount', 'payment_type', 'payment_approved']
admin.site.register(Payments, Payments_Admin)





class Inspection_Admin(admin.ModelAdmin):
    # search_fields = ['=id', 'condominio__rif', ]
    # list_filter = ('timestamp', 'fechafacturacion',)  
    # save_on_top = True
    # form = Egresos_Condominio_Form
    # def location_g(self, obj):
    #     lat = str(10.500000)
    #     lon = str(-66.916664)
    #     if lon and lat:
    #         url = 'https://www.google.com/maps/@%s,%s,10z' %(lat, lon)
    #         html ='<span>%s</span><a style="margin-left:10px;" href="%s"><b>%s</b></a>' % (obj.location, url, 'View in Google Maps')
    #         return html
    #     return 'Not Avaliable'
    # location_g.allow_tags = True
    # location_g.short_description = "Location"

    # def user_instance(self, obj):
    #     return obj
    #fields = [ 'created', 'origin', 'destination', 'description']
    fields = [ 'service' ,'description', 'inspection_type']
    #readonly_fields = ('parts_provider', 'description', 'location', 'service',)
    list_display  = [ 'service' ,'description', 'inspection_type']
admin.site.register(Inspections, Inspection_Admin)







# Register your models here.
class Auctions_Admin(admin.ModelAdmin):
    search_fields = ['host', 'title', 'auction_end', 'auction_begin' ]
    list_filter = ('host', 'city', 'state_providence', 'auction_end', 'auction_begin', 'country',)  
    # save_on_top = True
    # form = Egresos_Condominio_Form
    # fields = [  'monto', 'fechafacturacion', 'detalle', 'publicado']
    list_display =[
    'title',
    'host', 
    'created',
    'auction_begin',
    'auction_end',
    'address',
    'city',
    'state_providence',
    'country',
    'zip_code',
    'image'
    ]
admin.site.register(Auctions, Auctions_Admin)



class Inspection_ReportRowsInline(admin.TabularInline): 
    model = Inspection_Report_Rows
    #extra = 3
    def description_widget(self, obj):
        return obj.row.description
    description_widget.short_description = "Description"

    def rating_widget(self, obj):
        html_link = '%s' % (str(obj.rating) + ' stars' if not obj.rating == None else 'Not Rated')
        return html_link
    rating_widget.allow_tags = True


    fields = ['description_widget','rating_widget', 'details', 'item_picture']
    readonly_fields = ('description_widget','rating_widget',)
    def has_delete_permission(self, request, obj = None):
        return False

class Inspection_Report_Admin(admin.ModelAdmin):
    search_fields = ['created', 'lot_number', 'email', 'auction' ]
    list_filter = ('created',)  
    save_on_top = True
    inlines = (Inspection_ReportRowsInline,)
    # # form = Egresos_Condominio_Form
    # # fields = [  'monto', 'fechafacturacion', 'detalle', 'publicado']
    def auction(self, obj):
        return obj.inspection.service.auction_products.all().first().auction

    def lot_number(self, obj):
        return obj.inspection.service.auction_products.all().first().lot_number

    def email(self, obj):
        return obj.inspection.service.user.email

    readonly_fields = ['lot_number', 'email', 'auction', 'inspection']
    list_display = [
    'id',
    'inspection', 
    'created',
    'lot_number',
    'email',
    'auction'
    # 'auction_end',
    # 'address',
    # 'city',
    # 'state_providence',
    # 'country',
    # 'zip_code'
    ]
admin.site.register(Inspection_Reports, Inspection_Report_Admin)


class Inspection_Report_Rows_Admin(admin.ModelAdmin):
    pass
    # search_fields = ['host', 'title', 'auction_end', 'auction_begin' ]
    # list_filter = ('host', 'city', 'state_providence', 'auction_end', 'auction_begin', 'country',)  
    # # save_on_top = True
    # # form = Egresos_Condominio_Form
    # # fields = [  'monto', 'fechafacturacion', 'detalle', 'publicado']
    # list_display =[
    # 'title',
    # 'host', 
    # 'created',
    # 'auction_begin',
    # 'auction_end',
    # 'address',
    # 'city',
    # 'state_providence',
    # 'country',
    # 'zip_code'
    # ]
admin.site.register(Inspection_Report_Rows, Inspection_Report_Rows_Admin)



# class ProductsInline(admin.TabularInline): 
#     model = Auction_Products
#     extra = 3
#     # fields = ('id','item_name','auction', 'lot_number', 'image1',)
#     # readonly_fields = ('id','item_name','auction', 'lot_number', 'image1',)
#     def has_delete_permission(self, request, obj = None):
#         return False
# Register your models here.

class Items_Inline(admin.TabularInline): 
    model = Inspection_Types_Sections_Items
    extra = 0
    #fields = ( 'id', 'name')
    #readonly_fields = ('id','item_name','auction', 'lot_number', 'image1',)
    def has_delete_permission(self, request, obj = None):
        return True



class Inspection_Types_Sections_Inline(admin.TabularInline): 
    model = Inspection_Types.section.through
    extra = 0
    #fields = ( 'id', 'name')
    #readonly_fields = ('id','item_name','auction', 'lot_number', 'image1',)
    def has_delete_permission(self, request, obj = None):
        return True
    def has_change_permission(self, request, obj = None):
        return True

class Inspection_Types_Admin(admin.ModelAdmin):

    #inlines = (Inspection_Types_Sections_Inline,)
    #exclude = ('section',)
    #list_display = ['id', 'name', 'created', 'price', 'last_modified_ts']
    #list_display = [field.name for field in Inspection_Types._meta.fields if field.name != "id"]
    #fields = ('inspection_types_sections_set',)
    filter_horizontal = ('section',) 
admin.site.register(Inspection_Types, Inspection_Types_Admin)

class Inspection_Types_Admin_Items(admin.ModelAdmin):

    #inlines = (Inspection_Types_Sections_Inline,)
    exclude = ('rating', 'details', 'item_picture')
    list_display = ['description', 'section' ]
    list_filter = ('section',)
    list_editable = ('section', )
    #list_display = [field.name for field in Inspection_Types._meta.fields if field.name != "id"]
    #fields = ('inspection_types_sections_set',)
    #filter_horizontal = ('section',) 
admin.site.register(Inspection_Types_Sections_Items, Inspection_Types_Admin_Items)

class Inspection_Types_Sections_Admin(admin.ModelAdmin):
    inlines = (Items_Inline,)
    #list_display = ['id', 'name', 'created', 'last_modified_ts']
    

admin.site.register(Inspection_Types_Sections, Inspection_Types_Sections_Admin)


class Bank_Accounts_Admin(admin.ModelAdmin):
    list_display = ['bank', 'account_number' ,'routing_number', 'aba_number']
admin.site.register(Bank_Accounts, Bank_Accounts_Admin)

class Carousel_Image_Admin(admin.ModelAdmin):
    list_display = ['id', 'created' ,'counter','text', 'item_type','image', 'service']
    list_editable = ['item_type']
    form = CarouselItemsForm
    readonly_fields = ['counter']
    def save_model(self, request, obj, form, change):
        if len(Carousel_Image.objects.all())>=12:
            message= "You can not register more than 12 carousel items"
            messages.warning(request, message)
        super(Carousel_Image_Admin, self).save_model(request, obj, form, change)
admin.site.register(Carousel_Image, Carousel_Image_Admin)




class LogisticsInline(admin.StackedInline): 
    model = Logistics
    extra = 1
    #fields = ('description',)
    readonly_fields = ('id','description','origin', 'destination', 'origin_lat', 'origin_lon', 'destination_lat', 'destination_lon',)
    def has_delete_permission(self, request, obj = None):
        return False
    # def has_add_permission(self, request, obj = None):
    #     return True

class MaintenanceInline(admin.StackedInline): 
    model = Maintenance
    extra = 1
    #fields = ('description',)
    readonly_fields = ('maintenance_type','location','parts_provider', 'description',)
    def has_delete_permission(self, request, obj = None):
        return False
    # def has_add_permission(self, request, obj = None):
    #     return True




class InspectionsInline(admin.StackedInline):

    model = Inspections
    extra = 0

    def begin_inspection(self, obj):
        current_site = Site.objects.get_current().domain
        if obj.service.quote_payed and not obj.service.report:
            url = reverse('index') + 'admin/fill_inspection/%s' %(obj.pk)
            html_link = '<a href="%s">%s</a>' % (url, 'Fill Inspection')
            
            if obj.service.status == 'Resolved':
                url = reverse('index') + 'admin/userapp/inspection_reports/%s/change/' %(obj.inspection_reports.pk)
                html_link = '<a href="%s">%s</a>' % (url, 'View Report')
            return html_link
        return None

    begin_inspection.allow_tags = True
    fields = ('inspection_type', 'description','begin_inspection',)
    readonly_fields = ('inspection_type','description', 'begin_inspection',)
    
    def has_delete_permission(self, request, obj = None):
        return True
    # def has_add_permission(self, request, obj = None):
    #     return True



class Services_Admin(admin.ModelAdmin):
    # search_fields = ['host', 'title', 'auction_end', 'auction_begin' ]
    form = Inspection_ReportForm
    inlines = ()
    fields = ['status', 'quote_price', 'quote_file', 'quote_approved', 'resolved', 'solution_date','auction_products', 'report']
    list_display =[
    'service_type',
    'user_name',
    'id',
    'created',
    'status', 
    'quote_approved'
    ]

    readonly_fields = ( 'has_open_process', 'user_name', 'solution_date', 'auction_products', 'status',  'quote_approved', 'resolved', 'service_type',)
    #fields = []

    list_filter = ( 'status','service_type', )
    # # save_on_top = True

    def user_name(self, obj):
        return obj.user.get_full_name()

    def get_readonly_fields(self, request, obj=None):
        field_list =[]
        if obj:
            if obj.quote_price:
                #self.readonly_fields= self.readonly_fields+('quote_price',)
                field_list.append('quote_price')
            if obj.quote_file:
                field_list.append('quote_file')
                #self.readonly_fields = self.readonly_fields +('quote_file',)
            if not obj.report and obj.quote_payed == False:
                #self.readonly_fields = self.readonly_fields +('report',) 
                field_list.append('report')

            if obj.service_type =='Inspections' and not 'report' in field_list:
                field_list.append('report')
                    #return self.readonly_fields + ('quote_price',) + ('quote_file',)
                #return self.readonly_fields + ('quote_price',)
        total_list = self.readonly_fields+tuple(field_list)
        return total_list

    # def service_type(self, obj):
    #     return obj.service_type

    def change_view(self, request, object_id, form_url='', extra_context=None):
        instance = Services.objects.get(id = object_id)

        if instance.service_type =='Logistics':
            self.inlines = (LogisticsInline, )
        elif instance.service_type =='Maintenance':
            self.inlines = (MaintenanceInline, )
        elif instance.service_type =='Inspections':
            self.inlines = (InspectionsInline, )


        return super(Services_Admin, self).change_view(request, object_id)



    def save_model(self, request, obj, form, change):
        if obj:
            client = obj.user
            if obj.quote_price and form.has_changed():
                if 'quote_price' in form.changed_data and not form.initial['quote_price']:
                    obj.status = 'Quote Pending Client Approval'
                    obj.has_open_process = True
                    if obj.quote_file:
                        quote_origin = 'attachment'
                    else:
                        quote_origin = 'account'
                    email = EmailMessage(
                        'You have a new %s quote!' %(obj.service_type),
                        'Dear %s, you have a logistics quote pending your review'
                        '. Please read the information carefully in your %s. You may login to your' 
                        ' account at any time to reply to such quote.' %(client.get_full_name().title() or client, quote_origin),
                        settings.DEFAULT_FROM_EMAIL,
                        [client.email],
                        #['bcc@example.com'],
                        reply_to=[settings.LOGISTICS_EMAIL],
                        #headers={'Message-ID': 'foo'},
                    )

                    if obj.quote_file:
                        file = request.FILES.get('quote_file')
                        content_type = str(file.content_type)
                        file_name = str(file.name)
                        # attachment = open(file, 'rb')
                        email.attach(file_name, file.read(), content_type)
                    #send an email to user notifying that a quote was created
                    email.send()

                elif 'quote_file' in form.changed_data and obj.quote_file and not form.initial['quote_file']:
                    email = EmailMessage(
                        'You have a new logistics quote!',
                        'Dear %s, you have a logistics quote pending your review'
                        '. Please read the information carefully in your account or if this message includes an attachment. You may login to your' 
                        ' account at any time to reply to such quote.' %(client.get_full_name().title() or client),
                        settings.DEFAULT_FROM_EMAIL,
                        [client.email],
                        #['bcc@example.com'],
                        reply_to=[settings.LOGISTICS_EMAIL],
                        #headers={'Message-ID': 'foo'},
                    )

                    if obj.quote_file:
                        file = request.FILES.get('quote_file')
                        content_type = str(file.content_type)
                        file_name = str(file.name)
                        # attachment = open(file, 'rb')
                        email.attach(file_name, file.read(), content_type)
                    email.send()

                elif 'report' in form.changed_data:
                    subject = 'Your service report is now available!'
                    message = 'Dear %s, thank you for using Hecms, please find your service report attached in this message' %(client)

                    email = EmailMessage(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [client.email],
                        reply_to=[settings.LOGISTICS_EMAIL],
                    )

                    file = request.FILES.get('report', None)
                    if file:
                        content_type = str(file.content_type)
                        file_name = str(file.name)
                        # attachment = open(file, 'rb')
                        email.attach(file_name, file.read(), content_type)
                        email.send()    

        super(Services_Admin, self).save_model(request, obj, form, change)

admin.site.register(Services, Services_Admin)





# Register your models here.
class Auction_Products_Admin(admin.ModelAdmin):
    search_fields = ['lot_number', 'item_name' , 'user__email' ]


    def get_requested_services_url(self, obj):
        current_site = Site.objects.get_current()
        base_domain = current_site.domain
        services_list = []
        services_txt = ''
        product_services =list( obj.services_set.all())
        for service in product_services:
            if service.service_type == 'Maintenance':
                url = base_domain + 'admin/userapp/%s/%s/change/' %('maintenance', service.maintenance.pk)
                html_link = '<a href="%s">%s</a>' % (url, 'Maintenance')
                #services_list.append(html_link)
                services_txt += html_link if len(services_txt) == 0 else '<br>'+ html_link
            elif service.service_type == 'Logistics':
                url = base_domain + 'admin/userapp/%s/%s/change/' %('logistics', service.logistics.pk)
                html_link = '<a href="%s">%s</a>' % (url, 'Logistics')
                #services_list.append(html_link)
                services_txt += html_link if len(services_txt) == 0 else '<br>'+ html_link
            elif service.service_type == 'Inspections':
                url = base_domain + 'admin/userapp/%s/%s/change/' %('inspections', service.inspections.pk)
                html_link = '<a href="%s">%s</a>' % (url, 'Inspections')
                services_txt += html_link if len(services_txt) == 0 else '<br>'+ html_link

            
        return services_txt
    get_requested_services_url.short_description = "Services"
    get_requested_services_url.allow_tags = True


    readonly_fields = ('user',
        'auction',
        'lot_number',
        'image1',
        'get_requested_services_url',)
    
    #save_on_top = True
    fields = [  'lot_number', 'auction', 'user', 'image1', 'get_requested_services_url']
    list_display =[
    #'id',
    'lot_number',
    'item_name',
    'user',
    'auction',
    #'services',
    'get_requested_services_url',
    #'has_open_process'
    'image1'
    ] 
    #list_display_links = ('image1', )
admin.site.register(Auction_Products, Auction_Products_Admin)

# Register your models here.
class SampleCarouselServices_Admin(admin.ModelAdmin):

    #fields = [  'lot_number', 'auction', 'user', 'image1', 'get_requested_services_url']
    list_display = [ 'unique_id', 'object_type', 'report']
    readonly_fields = ['sample']
admin.site.register(SampleCarouselServices, SampleCarouselServices_Admin)


class SampleInspectionReportRow_Admin(admin.ModelAdmin):
    form=SampleReportForm
    #fields = [  'lot_number', 'auction', 'user', 'image1', 'get_requested_services_url']
    list_display = ['description','rating', 'image', 'section', 'inspection']
    # readonly_fields = ['sample']
admin.site.register(SampleInspectionReportRow, SampleInspectionReportRow_Admin)