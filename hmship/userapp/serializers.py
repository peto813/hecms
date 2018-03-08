import json
from rest_framework import serializers
from userapp.models  import *
from django.contrib.auth.models import User
from rest_auth.serializers import UserDetailsSerializer
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailConfirmation, EmailAddress
from rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from django.utils.translation import ugettext_lazy as _
from userapp.forms import customPasswordResetForm

service_types = ['logistics', 'inspections', 'maintenance']

#THIS FUNCTION SENDS EMAIL TO RECIPIENTS DEPENDING ON THE SERVICE TYPE THAT WAS REQUESTED
def Email_Confirmation_Message (section_type, user_recipient, admin_recipient, from_email, request, instance):
	#SEND EMAIL ADMIN
	user_instance  = request.user
	try:
		if not user_instance.first_name or not user_instance.last_name:
			full_name = 'Customer'
		else:
			full_name = ((user_instance.first_name )+' '+(user_instance.last_name)).title()
	except:
		full_name = 'Customer'

	from_email = settings.DEFAULT_FROM_EMAIL
	admin_email_dict =(
	'You have a new %s, request!' %(section_type),
	'Please check out your %s service requests in the admin panel. Hecms Web App' %(section_type),
	from_email,
	admin_recipient
	)

	#SEND EMAIL TO USER
	user_email_dict = (
	'Your %s request is being reviewed' %(section_type),
	'Dear %s, Thank you for requesting a service with Hecms, we will get back with you very shortly with a quote. Your ticket number is "%d" Have a nice day!' %( str(full_name), int(instance.id) ),
	from_email,
	[user_recipient]
	)

	msg_list = [admin_email_dict, user_email_dict]
	message_tuple = tuple(msg_list)
	send_mass_mail(message_tuple)

class Landing_Page_ImagesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Landing_Page_Images
		fields = '__all__'

class CarouselSerializer(serializers.ModelSerializer):
	class Meta:
		model = Carousel_Image
		fields = '__all__'


class AuctionsSerializer(serializers.ModelSerializer):

	service_type =  serializers.SerializerMethodField( read_only = True )

	class Meta:
		model = Auctions
		#fields = ( 'title', 'created' )
		fields = '__all__'
		#depth = 1

	def get_service_type(self,auction):
		return 'Auction'

class AuctionsField(serializers.Field):
	def to_representation(self, obj):
		auction = Auctions.objects.get(pk = obj.pk)
		serializer = AuctionsSerializer(auction)
		return serializer.data

	def to_internal_value(self, data):
		return Auctions.objects.get( id = data )



class Auction_ProductsSerializer(serializers.ModelSerializer):

	services = serializers.SerializerMethodField()
	auction = AuctionsField( )
	class Meta:
		model = Auction_Products
		fields = '__all__'	


	def validate_image1(self, value):
		if not value:
			return value
		#5 MB FILE VALIDATION
		if value.size >5242880:
			raise serializers.ValidationError("Image size too large")

		if value.size< 1024000:
			raise serializers.ValidationError("Image size too small")

		if not 'image/' in str(value.content_type):
			raise serializers.ValidationError("File type not accepted")
		return value

	def get_services(self, obj):
		output = { 'services_present': False, 'services_list' : 'None'}
		services = obj.services_set.all()	# profile = Profile.objects.get(pk=19)
		services_types = ', '.join(list(set([service.service_type for service in services])))
		if services and len( services ) > 0 :
			output = { 'services_present': True, 'services_list' : services_types }
		return output

	def __init__(self, *args, **kwargs):
		context = kwargs.pop( 'context', None )
		if context:
			request = context['request']
			if request.method == 'GET':
				query = request.GET.get('q')
				if query == 'editproducts' or query == 'logistics':
					self.fields['auction'] = AuctionsSerializer( read_only = True )
		super(Auction_ProductsSerializer, self).__init__(*args, **kwargs)

class PaypalSerializer(serializers.Serializer):
	service_id_list = serializers.PrimaryKeyRelatedField(many = True, queryset=Services.objects.filter( 
		quote_approved  = True, 
		has_open_process = True, 
		status = 'Pending Payment'
		))

	def create(self, validated_data):
		return validated_data


class ContactUsSerializer( serializers.Serializer ):
	CHOICES = (
		( 'product', 'product' ),
		( 'service', 'service' ),
		( 'suggestions', 'suggestions' ),
	)
	name = serializers.CharField(required = True, max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
	email = serializers.EmailField(required = True, max_length=None, min_length=None, allow_blank=False)
	subject = serializers.ChoiceField( CHOICES )
	message =  serializers.CharField(required = True, max_length=500, min_length=10, allow_blank=False, trim_whitespace=True)
    
	def save(self):
		send_mail(
			self.validated_data['subject'], 
			self.validated_data['message'], 
			self.validated_data['email'], 
			settings.ADMINISTRATIVE_EMAIL
			)

class updateEmailSerializer(serializers.ModelSerializer):
	email_confirm = serializers.CharField( required = True )

	class Meta:
		model = User
		fields = ['email', 'email_confirm']

	def validate_email(self, validated_data):
		email_exists = User.objects.filter(email = validated_data).exists()
		if email_exists:
			raise serializers.ValidationError("Email address already in use")
		return validated_data

	def validate(self, validated_data):
		email = validated_data['email']
		email_confirm = validated_data['email_confirm']
		if email != email_confirm:
			raise serializers.ValidationError("Email fields do not confirm")
		return validated_data

	def update(self, instance, validated_data):
		request = self.context['request']
		emailaddress = EmailAddress.objects.create(
			user= request.user,
			email = validated_data.get('email'),
			primary = True
			)
		instance.email = emailaddress.email
		instance.save()
		emailaddress.send_confirmation()
		return instance



# PARSES USER PASSWORD WHEN CHANGING
class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField( required = True )
    new_password = serializers.CharField( required = True, min_length = 8 )
    new_password_confirm = serializers.CharField( required = True )
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("Passwords do not confirm")
        return data


class deleteProductsSerializer(serializers.Serializer):
	del_list = serializers.PrimaryKeyRelatedField(many = True, queryset=Auction_Products.objects.all())

	def validate_del_list(self, data):
		user= self.context['request'].user
		for instance in data:
			if not instance.user == user:
				raise serializers.ValidationError("Forbidden object")
			if instance.services_set.all().exists():
				raise serializers.ValidationError("You can't delete products that have already been commited to a service")

		return data

	def create(self, validated_data):
		for instance in validated_data.get('del_list'):
			instance.delete()
		return validated_data



class LogisticsSerializer(serializers.ModelSerializer):
	origin = serializers.CharField( required  = False )
	class Meta:
		model = Logistics
		read_only_fields = (
			'service',
			'payment'
			)

		fields =  '__all__'

	def __init__(self, *args, **kwargs):
		method = kwargs.pop( 'method', None )
		if method == 'create':
			self.fields['products'] = serializers.ListField(
	   			child=serializers.IntegerField( min_value=0, required = True ) 
			)
		super(LogisticsSerializer, self).__init__(*args, **kwargs)

	def validate_products(self, validated_data):

		try:
			product_instance_list =[]
			for id in validated_data:
				product_instance = Auction_Products.objects.get(id = id)
				instance_services = product_instance.services_set.all()
				product_instance_list.append( product_instance )
				validated_data = product_instance_list
		except:
			raise serializers.ValidationError("Product Error")
		return validated_data

	def validate(self, validated_data ):
		request= self.context['request']
		unvalidated_data = request.data
		originSelect =  unvalidated_data.get('originSelect')
		if not originSelect:
			return validated_data

		if originSelect == 'other' and not unvalidated_data.get('otherOrigin'):
			raise serializers.ValidationError("No origin address")

		if originSelect == 'auction' or not originSelect:
			auction = validated_data.get('products')
			auction = list(validated_data.get('products'))[0].auction
			auction_data = {
			'address' : auction.address,
			'city' : auction.city,
			'state_providence' : auction.state_providence,
			'country' : auction.country,
			'zip_code' : auction.zip_code or ''
			}
			origin = str(auction_data['address']) + '' + str(auction_data['city']) +', ' + str(auction_data['state_providence']) + ', ' +  str(auction_data['country']) + ', '  +str(auction_data['zip_code'])
		else:
			origin = unvalidated_data.get('otherOrigin')
		validated_data['origin'] = origin
		return validated_data


	def create(self, validated_data):
		request = self.context['request']
		unvalidated_data = request.data
		products_data = validated_data.pop('products')
		service = Services.objects.create(user = request.user, service_type = 'Logistics')
		for product in products_data:
			service.auction_products.add( product )
		logistics = Logistics.objects.create( service  = service, **validated_data)
		Email_Confirmation_Message ('Logistics', request.user.email, settings.LOGISTICS_EMAIL, settings.DEFAULT_FROM_EMAIL, request, service)
		return logistics






class MaintenanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Maintenance
		fields = '__all__'
		read_only_fields = (
			'service',
			)
	def __init__(self, *args, **kwargs):
		method = kwargs.pop( 'method', None )
		if method == 'create':
			self.fields['products'] = serializers.IntegerField( min_value=0, required = True ) 
		super(MaintenanceSerializer, self).__init__(*args, **kwargs)

	def validate_products(self, validated_product_id ):

		#verify existence of product
		try:
			product = Auction_Products.objects.get(id = validated_product_id)
			#product exists make sure it does not have a relation to a maintenance service
			try:
				services = product.services_set.all()
				if services:
					for service in services:
						maintenance =  service.maintenance
						raise serializers.ValidationError("Product already has maintenace service")
			except:
				#ERROR IS RAISED BECAUSE THERE IS NO MAINTENANCE ASSOCIATED WITH IT return product
				return product
		except:
			raise serializers.ValidationError("Product does not exist!")

		return product

	def create(self, validated_data):
		request= self.context['request']
		service = Services.objects.create(user = request.user, service_type = 'Maintenance')
		unvalidated_data = request.data
		product = validated_data.pop('products')
		maintenance = Maintenance.objects.create( service  = service, **validated_data)
		maintenance.service.auction_products.add( product )
		Email_Confirmation_Message ('Maintenance', request.user.email, settings.MAINTENANCE_EMAIL, settings.DEFAULT_FROM_EMAIL, request, service)
		return maintenance


class UserProfileSerializer(serializers.ModelSerializer):

	class Meta:
		model = UserProfile
		fields = '__all__'


	def validate_profile_picture(self, value):
		if not value:
			return value
		#5 MB FILE VALIDATION
		if value.size >5242880:
			raise serializers.ValidationError("Image size too large")

		if value.size< 1024000:
			raise serializers.ValidationError("Image size too small")

		if not 'image/' in str(value.content_type):
			raise serializers.ValidationError("File type not accepted")
		return value

class Bank_AccountsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Bank_Accounts
		#fields = ['profile_picture']
		fields = '__all__'
		#depth = 1
		read_only_fields = ('bank', 'account_number', 'aba_number', 'details', 'address' , 'city',  'state_providence', 'zip_code', 'country', 'swift_number',  )




class UserSerializer(serializers.ModelSerializer):
	email_confirm = serializers.CharField( required = False )
	userprofile = UserProfileSerializer()
	class Meta:
		model = User
		fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True}
            }

	def validate_email(self, validated_data):
		email_exists = User.objects.filter(email = validated_data).exists()
		if email_exists:
			raise serializers.ValidationError("Email address already in use")
		return validated_data

	def validate(self, validated_data):


		email =  validated_data.get('email', None)
		email_confirm =  validated_data.get('email_confirm', None)
		if email:
			if email != email_confirm:
				raise serializers.ValidationError("Email fields do not confirm")

		return validated_data


	def update( self, instance, validated_data ):
		email =  validated_data.get('email', None)
		email_confirm =  validated_data.pop('email_confirm', None)

		if email and email_confirm:
			request = self.context['request']
			instance.email = validated_data.get( 'email', instance.email)
			emailaddress = EmailAddress.objects.create(
				user= request.user,
				email = email,
				primary = True
				)
			emailaddress.send_confirmation()
			instance.save()
			return instance

		instance.userprofile.company_name = validated_data.get( 'userprofile', None ).get( 'company_name', instance.userprofile.company_name )
		instance.first_name = validated_data.get('first_name', instance.first_name);
		instance.last_name = validated_data.get('last_name', instance.last_name);
		instance.save()
		return instance



class EditProductsSerializer(Auction_ProductsSerializer):
	auction = AuctionsSerializer( read_only = True)
	logistics = LogisticsSerializer( read_only = True )

	class Meta:
		model = Auction_Products
		fields = '__all__'


class Inspection_Types_Sections_Items_Serializer(serializers.ModelSerializer):
	section_name = serializers.SerializerMethodField(read_only = True)
	class Meta:
		model = Inspection_Types_Sections_Items
		fields = '__all__'
	def get_section_name(self, inspection_section_item):
		return inspection_section_item.section.name


class Inspection_Types_Sections_Serializer(serializers.ModelSerializer):
	#section_set = Inspection_Types_Sections_Items_Serializer(many = True)
	inspection_types_sections_items_set = Inspection_Types_Sections_Items_Serializer(many = True)
	class Meta:
		model = Inspection_Types_Sections
		fields = '__all__'

class Inspection_TypeSerializer(serializers.ModelSerializer):
	section = Inspection_Types_Sections_Serializer(many= True)
	class Meta:
		model = Inspection_Types
		fields = '__all__'
		#exclude = [ 'logistics', 'maintenance']
		#~fields = ['logistics', 'maintenance']
	
	# def validate_auction_products(self, validated_data):
	# 	return validated_data





class InspectionTypeField(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, obj):
    	serializer = Inspection_TypeSerializer(obj)
        return serializer.data

    def to_internal_value(self, data):
        return Inspection_Types.objects.get( id = data )


class InspectionReportSerializer(serializers.ModelSerializer):

	inspection_name = serializers.SerializerMethodField( read_only = True )
	sections = serializers.SerializerMethodField( read_only = True )

	class Meta:
		model = Inspection_Reports
		fields = '__all__'
		#depth = 5

	def get_inspection_name(self, obj):
		return obj.inspection.inspection_type.name

	def get_sections(self, obj):
		rows = obj.inspection.inspection_reports.inspection_report_rows_set.all()
		row_list = []
		for item in rows:
			row_dict = {
				'details': item.row.description,
				'rating': str(item.rating)
				#'item_picture': item.item_picture.path or ''
				#'': ''
			}
			row_list.append(row_dict)

		return row_list



class InspectionSerializer(serializers.ModelSerializer):
	inspection_type = InspectionTypeField()
	inspection_reports = InspectionReportSerializer(read_only = True)

	#inspection_type = Inspection_TypeSerializer()
	#inspection_type = serializers.PrimaryKeyRelatedField(queryset=Inspection_Types.objects.all() )
	class Meta:
		model = Inspections
		fields = '__all__'
		read_only_fields = (
			'service',
		)


	def __init__(self, *args, **kwargs):
		method = kwargs.pop( 'method', None )
		if method == 'create':
			self.fields['products'] = serializers.IntegerField( min_value=0, required = True ) 
		super(InspectionSerializer, self).__init__(*args, **kwargs)

	# def validate_inspection_type(self, data):
	# 	try:
	# 		instance = Inspection_Types.objects.get
	# 	except:
	# 		raise serializers.ValidationError("Invalid Service Type")
	# 	return data

	def validate_products(self, validated_product_id ):

		#verify existence of product
		try:
			product = Auction_Products.objects.get(id = validated_product_id)
			#product exists make sure it does not have a relation to a maintenance service
			try:
				services = product.services_set.all()
				if services:
					for service in services:
						inspections =  service.inspections
						raise serializers.ValidationError("Product already has maintenace service")
			except:
				#ERROR IS RAISED BECAUSE THERE IS NO MAINTENANCE ASSOCIATED WITH IT return product
				return product
		except:
			raise serializers.ValidationError( "Product does not exist!" )

		return product

	def create( self, validated_data ):
		request = self.context['request' ]
		#inspection_type = Inspection_Types.objects.get( id = )
		service = Services.objects.create( user = request.user, service_type = 'Inspections') 
		unvalidated_data = request.data
		product = validated_data.pop( 'products' )
		#maintenance = Maintenance.objects.create( **validated_data)
		#maintenance.maintenance_products.add( product )
		inspection = Inspections.objects.create( service  = service, **validated_data)
		inspection.service.auction_products.add( product )
		Email_Confirmation_Message ( 'Inspection', request.user.email, settings.LOGISTICS_EMAIL, settings.DEFAULT_FROM_EMAIL, request, service )
		return inspection




class ServiceSerializer(serializers.ModelSerializer):
	logistics = LogisticsSerializer( read_only = True)
	maintenance = MaintenanceSerializer( read_only = True)
	inspections = InspectionSerializer(read_only = True)
	auction_products = Auction_ProductsSerializer( many= True, read_only = True )

	class Meta:
		model = Services
		fields = '__all__'
		#exclude = [ 'logistics', 'maintenance']
		#~fields = ['logistics', 'maintenance']
		read_only_fields = ('user', 'service_type',)
	
	# def validate_auction_products(self, validated_data):
	# 	return validated_data

	# def to_representation(self, obj):
	# 	#service_types = ['logistics', 'inspections', 'maintenance']
	# 	# get the original representation

	# 	ret = super(ServiceSerializer, self).to_representation(obj)
	# 	service_type = str(ret['service_type']).lower()
	# 	for item in service_types:
	# 		if item != service_type :
	# 			del ret[item]
	# 	return ret

	def update(self, instance, validated_data, *args, **kwargs):
		request = self.context['request']
		quote_approved = validated_data.get('quote_approved')
		if quote_approved == True:
			resp = 'accepted'
		else:
			resp = 'rejected'
		subject = "%s has %s a %s quote!" %( str(request.user).title(), str(resp), str(instance.service_type))
		message = "%s has %s a %s quote! Go to Hecms admin panel, services, and review the payment information!" %( str(request.user).title(), str(resp), str(instance.service_type))
		sender = settings.DEFAULT_FROM_EMAIL
		recipient = settings.SERVICE_EMAIL
		send_mail(subject, message, sender, recipient)
		instance.quote_approved = quote_approved
		instance.save()
		return instance



class Services_Set_Field(serializers.Field):
    """
    Color objects are serialized into 'rgb(#, #, #)' notation.
    """
    def to_representation(self, instance):
        return instance.values()

    def to_internal_value(self, data):
    	try:
    		json_data  = json.loads(data)
    	except:
    		raise serializers.ValidationError("Input data error, only json accepted")
    	internal_value = [ Services.objects.get(pk = item['id']) for item in json_data ]
        return internal_value


class PaymentsSerializer(serializers.ModelSerializer):
	# auction = AuctionsSerializer( read_only = True)
	# logistics = LogisticsSerializer( read_only = True )
	# services_set = serializers.ListField(
	#    child=serializers.PrimaryKeyRelatedField( queryset = Services.objects.all(), 
	#    	required = True)
	# )
	services_set = Services_Set_Field( required = True )
	#services = ServiceSerializer( many = True )
	#service = serializers.PrimaryKeyRelatedField(queryset = Services.objects.all() ,many = True, required = True)
	#service_user = serializers.CharField(source = 'service.user', read_only= True)
	amount = serializers.DecimalField(read_only = True, max_digits=20, decimal_places=2)
	class Meta:
		model = Payments
		fields = '__all__'
		#read_only_fields = ('service_user',)
		#exclude = ['amount']
        # extra_kwargs = {
        #     # 'security_question': {'write_only': True},
        #     # 'security_question_answer': {'write_only': True},
        #     'services_set': {'write_only': True}
        #     }
	# def validate_user(self, validated_data):
	# 	return validated_data.email

	def create(self, validated_data):

		amount = 0
		services = validated_data.pop('services_set')
		new_services = []
		for service in services:
			service.status = 'Pending Hecms Approval'
			service.quote_payed = True
			service.save()
			new_services.append(service)
			amount+= service.quote_price

		payment = Payments.objects.create( amount =  amount, **validated_data )
		payment.services_set.set( new_services )
		return payment

class Inspection_Report_RowsSerializer( serializers.ModelSerializer ):
	row = Inspection_Types_Sections_Items_Serializer(read_only= True)
	section = serializers.SerializerMethodField(read_only=True)
	description = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = Inspection_Report_Rows
		fields = '__all__'
	def get_section(self, report_row):
		return report_row.row.section.name
	def get_description(self, report_row):
		return report_row.row.description

class InspectionCarouselSerializer(serializers.ModelSerializer):
	sections = serializers.SerializerMethodField(read_only= True)
	rows = serializers.SerializerMethodField(read_only= True)
	inspection = serializers.SerializerMethodField(read_only= True)
	service = serializers.SerializerMethodField(read_only= True)
	class Meta:
		model = Inspection_Reports
		fields = '__all__'

	def get_sections(self, inspection_report):
		#sections = set([{'name':item.row.section.name, 'id':str(item.row.section.id)} for item in inspection_report.inspection_report_rows_set.all()])
		sections = []
		for item in inspection_report.inspection_report_rows_set.all():
			sections.append({
				'name':item.row.section.name,
				'id':str(item.row.section.id)
			})
		sections = dict((v['id'],v) for v in sections).values()
		return sections
	def get_rows(self, inspection_report):
		rows = Inspection_Report_RowsSerializer(inspection_report.inspection_report_rows_set.all(), many = True)
		return rows.data

	def get_inspection(self, inspection_report):
		inspection = InspectionSerializer(inspection_report.inspection)
		return inspection.data

	def get_service(self, inspection_report):
		inspection = ServiceSerializer(inspection_report.inspection.service)
		return inspection.data


class CustomLoginSerializer(LoginSerializer):
	def validate(self, attrs):
		username = attrs.get('username')
		email = attrs.get('email')
		password = attrs.get('password')
		user = None
		if 'allauth' in settings.INSTALLED_APPS:
			from allauth.account import app_settings
			# Authentication through email
			if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
				user = self._validate_email(email, password)

			# Authentication through username
			if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
				user = self._validate_username(username, password)

			# Authentication through either username or email
			else:
				user = self._validate_username_email(username, email, password)

		else:
			# Authentication without using allauth
			if email:
				try:
					username = UserModel.objects.get(email__iexact=email).get_username()
				except UserModel.DoesNotExist:
					pass

			if username:
				user = self._validate_username_email(username, '', password)
		# Did we get back an active user?
		if user:
			if not user.is_active:
				msg = _('User account is disabled.')
				raise ValidationError(msg)
		else:
			msg = _('Unable to log in with provided credentials.')
			raise ValidationError(msg)

		# If required, is the email verified?
		if 'rest_auth.registration' in settings.INSTALLED_APPS:
			if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY and not user.is_staff:
				email_address = user.emailaddress_set.get(email=user.email)
				if not email_address.verified:
					raise serializers.ValidationError(_('E-mail is not verified.'))
		print 2.5
		attrs['user'] = user
		print 3
		return attrs

class customPasswordResetSerializer(PasswordResetSerializer):
	password_reset_form_class = customPasswordResetForm
	def validate_email(self, value):
		# Create PasswordResetForm with the serializer
		self.reset_form = self.password_reset_form_class(data=self.initial_data)
		try:
			email = User.objects.get(email = value)
		except:
			raise serializers.ValidationError(_("E-mail does not exist"))
		if not self.reset_form.is_valid():
			raise serializers.ValidationError(self.reset_form.errors)
		return value



class LandingPagecarouselSerializer(serializers.Serializer):
	unique_id = serializers.IntegerField(allow_null= True, required= False)
	obj_id = serializers.IntegerField(allow_null= True, required= False)
	image = serializers.ImageField()
	url = serializers.URLField(allow_null= True, required= False, allow_blank = True)
	object_type = serializers.CharField()
	sample = serializers.BooleanField(required = False)
	report = serializers.FileField()

class SampleInspectionReportRowSerializer(serializers.ModelSerializer):
	class Meta:
		model = SampleInspectionReportRow
		fields = '__all__'


class InspectionCarouselSampleSerializer(serializers.ModelSerializer):
	sections = serializers.SerializerMethodField(read_only= True)
	rows = serializers.SerializerMethodField()
	#inspection = serializers.SerializerMethodField(read_only= True)
	#service = serializers.SerializerMethodField(read_only= True)
	class Meta:
		model = SampleCarouselServices
		fields = '__all__'

	def get_sections(self, instance):
		rows= instance.rows.all()
		sections = [row.section for row in rows]
		return sections

	def get_rows(self, instance):
		rows = SampleInspectionReportRowSerializer(instance.rows.all(), many = True)
		return rows.data

	# def get_inspection(self, inspection_report):
	# 	inspection = InspectionSerializer(inspection_report.inspection)
	# 	return inspection.data

	# def get_service(self, inspection_report):
	# 	inspection = ServiceSerializer(inspection_report.inspection.service)
	# 	return inspection.data