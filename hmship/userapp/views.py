# -*- coding: utf-8 -*-

# encoding=utf8  
import sys , json, paypalrestsdk, paypalrestsdk, paypal, requests, dateutil.parser, decimal, random


reload(sys)  
sys.setdefaultencoding('utf8')
from django.utils.translation import ugettext_lazy as _
from userapp.models import *
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages, admin
from itertools import chain
from forms import *
from serializers import (

    Auction_ProductsSerializer,
    AuctionsSerializer,
    ChangePasswordSerializer,
    deleteProductsSerializer,
    LogisticsSerializer,
    MaintenanceSerializer,
    updateEmailSerializer,
    UserProfileSerializer,
    UserSerializer,
    Landing_Page_ImagesSerializer,
    EditProductsSerializer,
    ServiceSerializer,
    Inspection_TypeSerializer,
    InspectionSerializer,
    PaypalSerializer,
    Bank_AccountsSerializer,
    PaymentsSerializer,
    ContactUsSerializer,
    InspectionReportSerializer,
    CarouselSerializer,
    InspectionCarouselSerializer,
    CustomLoginSerializer,
    customPasswordResetSerializer,
    LandingPagecarouselSerializer,
    InspectionCarouselSampleSerializer
	)

from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from permissions import (
    IsOwnerOrReadOnly, 
    IsStaffOrReadOnly,
    IsOwner,
    isQuerySetOwner,
    )

from restful_filters import (
    Products_Filter, 
    Services_Filter,
    AuctionFilter,
    Payments_Filter,
    )

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
	#DJANGO FRAMEWORK
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

		#REST FRAMEWORK
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    RetrieveAPIView,
    UpdateAPIView,
    ListCreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
    ListAPIView,
    )
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
#from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
#REST AUTH
from rest_auth.views import LoginView, PasswordResetView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.registration.views import SocialLoginView

#ALLAUTH DEPENDENCIES
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from allauth.account.models import EmailAddress
##############TWIITER AUTH#################
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from rest_auth.views import LoginView




class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer


# Create your views here.
def index(request):
    # peo = Inspection_Types_Sections.objects.all().first()
    context = {
        'title':'HM-Ship | Welcome'
    }
    if ('oauth_token' and 'oauth_verifier') in str(request.GET):
        data = {}
        oauth_verifier = request.GET.get('oauth_verifier')
        oauth_token = request.GET.get('oauth_token')
        if oauth_token:
            oauth = OAuth1(settings.CONSUMER_KEY,
                           client_secret=settings.CONSUMER_SECRET,
                           resource_owner_key=oauth_token,
                           resource_owner_secret=oauth_verifier,
                           verifier=oauth_verifier)

            r = requests.post( url = settings.ACCESS_TOKEN_URL, auth = oauth )
            if not r.status_code == 401 :
                credentials = parse_qs( r.content )
                data[ 'token_secret' ] = credentials[ 'oauth_token_secret' ]
                data[ 'access_token' ] = credentials[ 'oauth_token' ]
                r = requests.post( '%s://%s/rest-auth/twitter/' %( settings.HTTP_PROTOCOL, request.get_host() ), data = data, timeout = 5 ).json()[ 'key' ] #auth=('user', 'pass')
                if r:
                    context[ 'title' ] = 'HM-Ship | Twitter Redirect'
                    context[ 'tokenDict' ] = json.dumps( r )

    return render(request, 'index.html', context)

@staff_member_required
def inspection_report_success( request):
    context = {
        'title':'Hecms | Inspection report Success'
    }
    return render(request, 'inspection_report_succes.html', context)

@staff_member_required
def fill_inspection( request, inspection_id = None ):
    inspection = Inspections.objects.get(pk=inspection_id)
    if request.method == 'POST':
        data = list(request.POST.copy())
        report_row_obj_list = []
        report_created = False
        item_id_list = []
        for item in data:
            cleaned_item_string =  str(item).replace('item_rating_', '').replace('item_details_', '').replace('item_pic_', '')
            if cleaned_item_string.isdigit():
                item_id_list.append(int(cleaned_item_string))

        item_id_list = list(set(item_id_list))
        for item_id in item_id_list:
            details = request.POST.get( 'item_details_%s' %( str(item_id) ) ) or 'N/A'
            rating = request.POST.get( 'item_rating_%s' %( str(item_id) ) ) or None
            item_picture = request.FILES.get( 'item_pic_%s' %( str(item_id) ) ) or None
            data_set = {
                'row' : item_id, #inspection section item id (must be instance)
                'rating': rating, #rating for the item that will go in report
                'details': details #inspection details for the item that will go in report
            }
            item_picture_dict = {
                'item_picture' : item_picture or None
            }
            form_row = Inspection_Row_Form(data_set, item_picture_dict)
            if form_row.is_valid():
                if not report_created:
                    report = Inspection_Reports.objects.create(inspection = inspection)
                    report_created = True
                    form_row_instance = form_row.save(commit = False)
                    form_row_instance.inspection_report = report
                    form_row_instance.save()
            
                else:
                    form_row_instance = form_row.save(commit = False)
                    form_row_instance.inspection_report = report
                    form_row_instance.save()
            else:
                #message = str(form_row.errors)
                #send_mail('error', message, 'webmaster@hecms.net', ['peto813@gmail.com'])
                context = {
                    'title':'Hecms | Fill Inspection Report',
                    'inspection': inspection,
                    'form_row':form_row
                }
                return render(request, 'fill_inspection.html', context)


        inspection.service.status = 'Resolved'
        inspection.service.has_open_process = False
        inspection.service.save()
        subject = "Your item has been inspected!" 
        message = "Dear customer, your inspection service request #%s has been fulfilled, to view it log in to your account, go to manage orders-orderbook tab" %(str(inspection.service.id))
        sender = settings.DEFAULT_FROM_EMAIL
        recipient = [str(inspection.service.user.email)]
        send_mail(subject, message, sender, recipient)
        return HttpResponseRedirect(reverse('inspection_report_success'))


    context = {
        'title':'Hecms | Fill Inspection Report',
        'inspection': inspection
    }
    return render(request, 'fill_inspection.html', context)



######################################  TWITTER APP #################################

class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter

class TwitterOauth(APIView):
    renderer_classes = (JSONRenderer, )
    def get(self, request):
        # Request oauth token
        oauth = OAuth1(settings.CONSUMER_KEY, client_secret=settings.CONSUMER_SECRET)
        r = requests.post(url=settings.REQUEST_TOKEN_URL, auth=oauth)
        credentials = parse_qs(r.content)
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]

        #DJANGO SESSION STORES CREDENTIALS
        #request.session['resource_owner_key'] = resource_owner_key
        #request.session['resource_owner_secret'] = resource_owner_secret

        # Authorize url
        authorize_url = settings.AUTHORIZE_URL + resource_owner_key

        return Response(authorize_url)


# def Twitter_Callback_View(request):
#     #if ('oauth_token' and 'oauth_verifier') in str(request.GET):
#     #try:
#             #if ('oauth_token' and 'oauth_verifier') in str(request.GET):
#     context = {
#         'title':'HM-Ship | Twitter Redirect'
#     }

#     data = {}
#     oauth_verifier = request.GET.get('oauth_verifier')
#     oauth_token = request.GET.get('oauth_token')
#     #resource_owner_key = request.session['resource_owner_key']
#     if oauth_token:
#         oauth = OAuth1(settings.CONSUMER_KEY,
#                        client_secret=settings.CONSUMER_SECRET,
#                        resource_owner_key=oauth_token,
#                        resource_owner_secret=oauth_verifier,
#                        verifier=oauth_verifier)

#         #del request.session['resource_owner_key']
#         #del request.session['resource_owner_secret']
#         r = requests.post( url = settings.ACCESS_TOKEN_URL, auth = oauth )
#         if not r.status_code == 401 :
#             credentials = parse_qs( r.content )
#             data[ 'token_secret' ] = credentials[ 'oauth_token_secret' ]
#             data[ 'access_token' ] = credentials[ 'oauth_token' ]
#             r = requests.post( 'http://%s/rest-auth/twitter/' %( request.get_host() ), data = data, timeout = 5 ).json()[ 'key' ] #auth=('user', 'pass')
#             if r:
#                 context[ 'title' ] = 'HM-Ship | Twitter Redirect'
#                 context[ 'tokenDict' ] = json.dumps( r )
#                 # context = {
#                 #     'title':'HM-Ship | Twitter Redirect',
#                 #     'tokenDict' : json.dumps(r)
#                 # }
#             # else:
#             #     pass

    
#     return render(request, 'twitter_callback.html', context)
    # except:
    #     context = {
    #         'title':'HM-Ship | Twitter Redirect',
    #         'tokenDict' : 'Error'
    #     }
        #return render(request, 'twitter_callback.html', context)


#################################### PAYPALL APP #########################

def Paypal_Return_View(request):
    if request.method == 'GET':
        data = request.GET.copy()
        payment = paypalrestsdk.Payment.find(data['paymentId'])
        items = payment.transactions[0]['item_list']['items']
        services = Services.objects.filter(pk__in = [item.sku for item in payment.transactions[0]['item_list']['items'] ])
        user = services.first().user
        if payment.execute({"payer_id": data['PayerID']}):
            services.update(status="Payed", quote_payed = True, has_open_process = False )
            data = {
                'payment_approved': True,
                'payment_approved' : True,
                'payment_type' : 'paypal',
                'created' : dateutil.parser.parse(payment.create_time),
                'amount' : decimal.Decimal(payment.transactions[0]['amount']['total']),
                'user' : user
            }

            payment = Payments.objects.create(**data)
            payment.services_set.set( services )


            #EMAIL ADMIN
            #messages.add_message(request, messages.INFO, 'Car has been sold')
            subject = "You have a new payment for service"
            message = "%s has made a payment via %s for an amount of %s" %( str(user.email).title() , str( payment.payment_type ), str(payment.amount) )
            sender = settings.DEFAULT_FROM_EMAIL
            recipient = settings.SERVICE_EMAIL
            send_mail(subject, message, sender, recipient)

            redirect_url = get_current_site(request).domain + '#/home'
            context = {
                'title':'Paypal Payment Accepted',
                'services': services,
                'payment' : payment,
                'payment_status' : 'success',
                'redirect_url' : redirect_url
            }
            return render(request, 'paypal_accepted.html', context)


        #payment.execute({"payer_id": data['PayerID']})

    context = {
        'title':'Paypal Payment Accepted'
        #'facebook_app_id' : settings.FACEBOOK_APP_ID
    }
    return render(request, 'paypal_accepted.html', context)
# class twitter_login(APIView):
#     #carousel_images = 
#     renderer_classes = (JSONRenderer, )
#     def get(self, request):
#     #if request.method =='GET':
#         if ('oauth_token' and 'oauth_verifier') in str(request.GET):
#             data = {}
#             oauth_verifier = request.GET.get('oauth_verifier')
#             oauth_token = request.GET.get('oauth_token')
#             resource_owner_key = request.session['resource_owner_key']
#             if resource_owner_key == oauth_token:
#                 oauth = OAuth1(settings.CONSUMER_KEY,
#                                client_secret=settings.CONSUMER_SECRET,
#                                resource_owner_key=resource_owner_key,
#                                resource_owner_secret=request.session['resource_owner_secret'],
#                                verifier=oauth_verifier)

#                 del request.session['resource_owner_key']
#                 del request.session['resource_owner_secret']
#                 r = requests.post(url=settings.ACCESS_TOKEN_URL, auth=oauth)
#                 credentials = parse_qs(r.content)
#                 data['token_secret'] = credentials['oauth_token_secret']
#                 data['access_token'] = credentials['oauth_token']
#                 r = requests.post('http://%s/rest-auth/twitter/' %(request.get_host()), data=data ).json() #auth=('user', 'pass')
                
#                 context = {
#                     'title':'HM-Ship | Welcome',
#                     'token' : r
#                 }

#                 return render(request, 'index.html', context)
# http://peto813.ddns.net:9000/rest-auth/registration/account-confirm-email/1/
# http://peto813.ddns.net:9000/rest-auth/registration/account-confirm-email/OQ:1cfq0i:hJxPdKWA3GZ5fq28bnF9eEHeH_c/


class confirmEmailView(TemplateView):
    template_name = "email_confirm.html"
    def get_context_data(self, **kwargs):
        if kwargs['key']:
            secure = self.request.is_secure()
            protocol = 'https' if secure==True else 'http'
            url = '%s://%s%s' %( protocol, self.request.get_host(), reverse('rest_verify_email'))
            r = requests.post(url, data = kwargs )
            if r.status_code == 200:
                account_verified  = True
            else:
                account_verified = False

        context = super( confirmEmailView, self ).get_context_data(**kwargs)
        context['account_verified'] = account_verified
        return context

#SOCIAL APP VIEWS
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    #permission_classes = ( AllowAny, )


    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        try:
            self.serializer.is_valid(raise_exception=True)
            self.login()
            return self.get_response()
        except:
            return Response( 'There is already an account using this E-mail address, perhaps you have registered with an E-mail account.', status = status.HTTP_400_BAD_REQUEST )


class GoogleLogin(SocialLoginView):
    #serializer_class = TwitterLoginSerializer
    adapter_class = GoogleOAuth2Adapter


class AuctionsViewSet(viewsets.ModelViewSet):
    queryset = Auctions.objects.all()
    serializer_class = AuctionsSerializer
    permission_classes = ( IsAuthenticated, IsStaffOrReadOnly )
    #queryset = Services.objects.all()
    #serializer_class = ServiceSerializer
    filter_backends = ( DjangoFilterBackend, )
    filter_class = AuctionFilter
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = AuctionsSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)


    #queryset = self.get_queryset()
    #serializer = UserSerializer(queryset, many=True)


class ContactUsView( APIView ):
    def post(self, request, format = None):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('success', status=status.HTTP_200_OK)
        return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )


class AuctionsProductsViewSet(viewsets.ModelViewSet, GenericAPIView):
    queryset = Auction_Products.objects.all()
    serializer_class = Auction_ProductsSerializer
    filter_backends = ( DjangoFilterBackend, )
    filter_class = Products_Filter
    permission_classes = ( 
        IsAuthenticated, 
        IsOwner,
        )


    def get_object(self, pk):
        try:
            obj =  Auction_Products.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Auction_Products.DoesNotExist:
            raise Http404


    def get_queryset(self):
        return Auction_Products.objects.filter(user=self.request.user.id)

    def get_serializer_context(self):
        return { 'request': self.request }

    # def get_queryset(self):
    #     auction_products = Auction_Products.objects.filter(user = self.request.user)
    #     return auction_products
    # def get_queryset(self):
    #     queryset_list = self.queryset.filter(user = self.request.user)
        
    #     query = self.request.GET.get('q')

    #     if query == 'logistics':
    #         queryset_list = queryset_list.exclude( services__logistics__isnull = False )

    #     elif query == 'inspections':
    #         queryset_list = queryset_list.exclude( services__inspections__isnull = False )
            
    #     elif query == 'maintenance':
    #         queryset_list = queryset_list.exclude( services__maintenance__isnull = False )
    #     return queryset_list

    # def list(self, request):
    #     serializer = self.get_serializer( self.get_queryset(), many= True )
    #     return Response(serializer.data)

    def create( self, request ):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status = status.HTTP_200_OK )
        else:
            return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )


class InspectionReportViewSet(viewsets.ModelViewSet):
    serializer_class = InspectionReportSerializer
    permission_classes = ( 
        #IsAuthenticated,
        #IsOwner,
        IsStaffOrReadOnly,
        #AllowAny,
        )
    queryset = Inspection_Reports.objects.all()

    def get_object(self, pk = None):
        try:

            obj =  Inspection_Reports.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Inspection_Reports.DoesNotExist:
            raise Http404
    # def get(self, request):
    #     serializer = self.get_serializer(self.get_queryset())
    #     return Response(serializer.data)


class Bank_AccountsViewSet(viewsets.ModelViewSet):
    serializer_class = Bank_AccountsSerializer
    permission_classes = ( 
        IsStaffOrReadOnly,
        )
    queryset = Bank_Accounts.objects.all()

    # def get(self, request):
    #     serializer = self.get_serializer(self.get_queryset())
    #     return Response(serializer.data)

class PaymentsViewSet(viewsets.ModelViewSet):
    
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = ( DjangoFilterBackend, )
    filter_class = Payments_Filter
    permission_classes = ( 
        IsAuthenticated, 
        IsOwner,
        )
    # def get(self, request):
    #     serializer = self.get_serializer(self.get_queryset())
    #     return Response(serializer.data)
    def get_object(self, pk):
        try:

            obj =  Payments.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Payments.DoesNotExist:
            raise Http404

    def get_queryset(self):
        payments = Payments.objects.filter(user = self.request.user)
        return payments

    # def list(self, request):
    #     # serializer = Auction_ProductsSerializer( 
    #     #     Auction_Products.objects.filter(user = request.user), many= True, context={'request': request} )
    #     serializer = self.get_serializer(self.queryset.filter(user = request.user), many= True)
    #     return Response(serializer.data)

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.pk
        serializer = self.get_serializer( data = data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EditProductsViewSet(AuctionsProductsViewSet):
    serializer_class = EditProductsSerializer
    permission_classes = ( 
        IsAuthenticated,
        IsOwner,
        )

    def get_object(self, pk):
        try:

            obj =  Auction_Products.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Auction_Products.DoesNotExist:
            raise Http404

    def update(self, request, pk, format=None):
        snippet = self.get_object(pk)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response('serializer.data', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#view that approves or rejects service quotes
class ServicesViewSet(viewsets.ModelViewSet): # removed AuctionsProductsViewSet from this class init
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = ( DjangoFilterBackend, )
    filter_class = Services_Filter
    #queryset = Services.objects.all()
    permission_classes = ( 
        IsAuthenticated, 
        IsOwner,
        )

    def get_object(self, pk):
        try:
            obj =  Services.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Services.DoesNotExist:
            raise Http404

    def partial_update(self, request, pk = None):
        instance = self.get_object(pk)
        serializer = ServiceSerializer(instance, data = request.data, partial=True, context = {'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    # def update(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     data = request.data.copy()
    #     data['user'] = request.user.id
    #     serializer = self.get_serializer(snippet, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LandingPageView(ListAPIView):
    queryset = Landing_Page_Images.objects.all()

    def check_service(self, queryset, service_type):
        diff = 4-len(queryset)
        if diff >0:
            queryset= SampleCarouselServices.objects.filter(service_type='Logistics')[:diff]
        return queryset

    def get_service_count(self, services):
        logistics = 0
        inspections = 0
        maintenance = 0
        for item in services:
            if item['object_type'] =='Logistics':
                logistics+=1
            elif item['object_type'] =='Inspections':
                inspections+=1
            elif item['object_type'] =='Maintenance':
                maintenance+=1
        count = {
            'Logistics' :logistics,
            'Maintenance' :maintenance,
            'Inspections' :inspections,
        }
        return count

    def list(self, request):

        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = Landing_Page_ImagesSerializer(queryset, many=True)
        carousel_list = []
        try:
            logistics = [item.service for item in Logistics.objects.filter(service__resolved = True).order_by('-service__created')[:4]]
            maintenace = [item.service for item in Maintenance.objects.filter(service__resolved = True).order_by('-service__created')[:4]]
            inspections =[item.service for item in Inspections.objects.filter(service__resolved = True).order_by('-service__created')[:4]]
            if inspections or maintenace or logistics:
                images_present = True
            else:
                images_present = False
        except:
            images_present = False


        if images_present:
            normalize_services = inspections+logistics+maintenace

            # normalize_services = inspections+logistics+maintenace
            service_list = []
            counter = 0
            for service in normalize_services:
                data={
                    'obj_id':service.id,
                    'url': None,
                    'object_type': service.service_type,
                    'image':service.auction_products.first().image1,
                    'unique_id' :counter,
                    'sample': False
                }
                service_list.append(data)
                counter +=1

            carousel_list = service_list

            # while len(carousel_list)<12:
            #     carousel_list.append(carousel_list[random.randint(0, len(carousel_list)-1)])
            #     counter +=1

            #serializer_x = LandingPagecarouselSerializer(carousel_list, many = True).data
        #else:
            #serializer_x = None
        service_details = self.get_service_count(carousel_list)
        samples = SampleCarouselServices.objects.all()
        for key, count in service_details.iteritems():
            if key == 'Logistics':
                logistics_samples=samples.filter(object_type=key)[:4]

                for item in logistics_samples:
                    carousel_list.append(item)

            elif  key =='Inspections':
                inspections_samples=samples.filter(object_type=key)[:4]
                for item in inspections_samples:
                    carousel_list.append(item)

            elif key =='Maintenance':
                maintenance_samples=samples.filter(object_type=key)[:4]
                for item in maintenance_samples:
                    carousel_list.append(item)


        serializer_x = LandingPagecarouselSerializer(carousel_list, many = True).data

        auctions = Auctions.objects.order_by('-created')[:8]
        auction_serializer = AuctionsSerializer(auctions, many=True)
        context = {
            'landing_page_imageri':serializer.data,
            'carousel_gallery' : serializer_x,
            'auctions': auction_serializer.data
        }     


        return Response(context)

class CreateOrUpdatePicView(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = UserProfileSerializer
    model = UserProfile

    permission_classes = (
    	IsAuthenticated,
    	#AllowAny,
    	)

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer( data = request.data )
        if serializer.is_valid():
            cd =  serializer.validated_data
            try:
                obj = UserProfile.objects.get(user=request.user)
                obj.company_name = cd.get('company_name')
                obj.profile_picture = cd.get('profile_picture')

            except UserProfile.DoesNotExist:
                obj = UserProfile( user = request.user, company_name=cd.get('company_name'), profile_picture = cd.get('profile_picture') )
            
            obj.save()
            serializer = UserProfileSerializer(obj)
            return Response( serializer.data )
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format = None):
        try:
            user_obj = UserProfile.objects.get(user = request.user)
            user_obj.profile_picture = None
            user_obj.save()
            serializer = UserProfileSerializer(user_obj)
            return Response(serializer.data)
        except:
            return Response("No Picture object", status=status.HTTP_400_BAD_REQUEST)


class customPasswordResetView(PasswordResetView):
    serializer_class = customPasswordResetSerializer
    #serializer_class = customPasswordResetSerializer
    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return the success message with OK HTTP status
            return Response(
                {"detail": _("Password reset e-mail has been sent.")},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteProductsViewSet( viewsets.ModelViewSet ):
    queryset = Auction_Products.objects.all()
    serializer_class = deleteProductsSerializer
    permission_classes = (  
        IsAuthenticated, 
        #IsOwnerOrReadOnly,
    )
    def create( self, request ):
        serializer = deleteProductsSerializer( data = request.data, context = {'request': request} )
        if serializer.is_valid( ):
            serializer.save()
            auction_products = Auction_Products.objects.filter( user = request.user )
            serializer = Auction_ProductsSerializer(auction_products, many  = True)
            return Response( serializer.data, status = status.HTTP_200_OK )
        return Response( serializer.errors, status = status.HTTP_400_BAD_REQUEST )


class LogisticsViewSet(viewsets.ModelViewSet):
    queryset = Logistics.objects.all()
    serializer_class = LogisticsSerializer
    permission_classes = (  
        IsAuthenticated, 
        IsOwner,
    )

    # def get_queryset(self):
    #     return Logistics.objects.filter(user__services__user = self.request.user)
    # def get_object(self, pk ):
    #     try:
    #         return Logistics.objects.get(pk=pk)
    #     except Logistics.DoesNotExist:
    #         raise Http404

    # def list(self, request):
    #     serializer = Auction_ProductsSerializer( 
    #         Auction_Products.objects.filter(user = request.user), many= True, context={'request': request} )
    #     return Response(serializer.data)

    def create(self, request):
        data = request.data.copy()
        serializer = LogisticsSerializer( data = data, context = {'request': request}, method = 'create' )
        if serializer.is_valid():
            serializer.save()
            #serializer = Auction_ProductsSerializer( 
            #Auction_Products.objects.filter(user = request.user), many= True )
            return Response('Success', status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


        # serializer = self.get_serializer(snippet, data = request.data, partial = True)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        # return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        # snippet = self.get_object(pk)
        # data = request.data.copy()
        # data['user'] = request.user.id
        # serializer = self.get_serializer(snippet, data=data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = (  
        IsAuthenticated, 
        IsOwner,
    )

    # def list(self, request):
    #     serializer = Auction_ProductsSerializer( 
    #         Auction_Products.objects.filter(user = request.user).filter(maintenance__isnull = True), many= True )
    #     return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data= request.data, context = {'request': request}, method = 'create')
        if serializer.is_valid():
            serializer.save()
            return Response('Success', status=status.HTTP_200_OK)
        else:    
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class InspectionTypesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inspection_Types.objects.all()
    serializer_class = Inspection_TypeSerializer
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
    )

class InspectionsViewSet(viewsets.ModelViewSet):
    queryset = Inspections.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = (  
        IsOwner, 
        IsAuthenticated, 
    )

    # def list(self, request):
    #     serializer = Auction_ProductsSerializer( 
    #         Auction_Products.objects.filter(user = request.user).filter(maintenance__isnull = True), many= True )
    #     return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data= request.data, context = {'request': request}, method = 'create')
        if serializer.is_valid():
            serializer.save()
            return Response('Success', status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



# class OrderBookViewSet( viewsets.ModelViewSet ):
#     queryset = Services.objects.all( )
#     serializer_class = ServiceSerializer
#     permission_classes = (  
#         #AllowAny, 
#         IsAuthenticated, 
#     )
#     #filter_backends = ( DjangoFilterBackend, )
#     #filter_class = Services_Filter

#     def get_queryset(self):
#         services = Services.objects.filter(user = self.request.user)
#         return services

#     def list(self, request):
#         serializer = self.get_serializer( self.get_queryset(), many= True )
#         return Response(serializer.data)

    # def get_queryset(self):
    #     user = self.request.user
    #     return Services.objects.filter(user=user).filter( Q(maintenance__isnull = False) | Q(logistics__isnull = False) )

    # def list(self, request):
    #     serializer = 
    #     return Response(serializer.data)
    #def list( self, request ):
        #result_list = list(chain(page_list, article_list, post_list))
        # auctions = Auction_Products.objects.filter(user = request.user).filter(
        #         Q(maintenance__isnull = False) | Q(logistics__isnull = False)
        #         )
        # def add_identifier_field(item_list, identifier):
        #     for item in item_list:
        #         item.status = getattr(item, identifier).status
        #         item.identifier = identifier
        #     return item_list

        # user_auctions = Auction_Products.objects.filter(user = request.user).select_related()
        # maintenance = add_identifier_field(user_auctions.filter(maintenance__isnull = False).filter(maintenance__resolved = False), 'maintenance')
        # logistics = add_identifier_field(user_auctions.filter(logistics__isnull = False).filter(logistics__resolved = False), 'logistics')
        # result_list = list(chain(maintenance, logistics))
        # serializer = Auction_ProductsSerializer( result_list, many= True )
        #return Response(serializer.data)

    # def create(self, request):
    #     serializer = MaintenanceSerializer(data= request.data, context = {'request': request})
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response('Success', status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class PaypalView(APIView):
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
    )
    renderer_classes = (JSONRenderer, )
    # def get_queryset(self):
    #     queryset_list = Services.objects.filter(user = self.request.user)
    #     return queryset_list

    def post(self, request, format=None):

        serializer = PaypalSerializer( data = request.data)
        if serializer.is_valid():
            payment = paypal.create_payment( request, serializer.validated_data['service_id_list'])
            for link in payment.links:
                if link.rel == 'approval_url':
                    return Response(link.href, status=status.HTTP_200_OK)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
        IsOwner,
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            obj = User.objects.get(id=pk)
            self.check_object_permissions(self.request, obj)
            return obj

        except User.DoesNotExist:
            raise Http404

    def get_queryset(self):
        return self.queryset.filter(id = self.request.user.id)


    def partial_update(self, request, pk = None):

        instance = self.get_object( pk=pk)
        serializer = self.get_serializer(instance, data = request.data, partial=True, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def retrieve(self, request, pk=None):
    #     #queryset = User.objects.all()
    #     #user = get_object_or_404( self.get_queryset(), pk=1 )
    #     serializer = UserSerializer(self.get_queryset())
    #     return Response(serializer.data)

    # def get(self, request):
    #     serializer = UserSerializer(self.get_queryset())
    #     return Response(serializer.data)

#GETS THE USER DETAILS WHEN LOGIN
class UserDetailsView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all( )
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
        IsOwner,
         #IsOwnerOrReadOnly,
    )

    def get_object(self, pk):
        try:
            obj = UserProfile.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj

        except UserProfile.DoesNotExist:
            raise Http404

    def partial_update(self, request, pk = None):
        instance = self.get_object( pk=pk )
        data = request.data.copy()
        if 'profile_picture' in data.keys():
            data['profile_picture'] = None if (data['profile_picture'] == ''or data['profile_picture'] == None ) else data['profile_picture']
        # if profile_picture in data:
        serializer = self.get_serializer(instance, data = data, partial=True, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_queryset(self):
#         queryset_list, created = self.queryset.get_or_create(user = self.request.user)
#         return queryset_list


#     def patch(self, request, pk = None):
#         queryset = self.get_queryset()
#         data = request.data.copy()
#         data['user'] = self.request.user.pk
#         serializer = UserProfileSerializer(queryset, data = data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#         #return Response('testing', status=status.HTTP_200_OK)
#         return Response('serializer.data', status=status.HTTP_400_BAD_REQUEST)


class upDateEmailView(APIView):
    def put(self, request ):
        serializer = updateEmailSerializer(instance = request.user, data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=status.HTTP_200_OK)
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )




class InspectionCarouselView(APIView):
    permission_classes = ( IsAuthenticatedOrReadOnly, )
    def get(self, request, service = None):
        try:
            obj =  Inspection_Reports.objects.get(inspection__service__pk=service)
            serializer= InspectionCarouselSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response( 'NOT FOUND', status=status.HTTP_400_BAD_REQUEST )

class InspectionCarouselSampleView(RetrieveAPIView):
    permission_classes = ( IsAuthenticatedOrReadOnly, )
    queryset = SampleCarouselServices.objects.all()
    def get(self, request, service = None):
        instance=self.queryset.get(pk=service)
        serializer = InspectionCarouselSampleSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK) 
        # try:
        #     obj =  Inspection_Reports.objects.get(inspection__service__pk=service)
        #     serializer= InspectionCarouselSerializer(obj)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # except:
        #     return Response( 'NOT FOUND', status=status.HTTP_400_BAD_REQUEST )

class LogisticsCarouselViewSet(viewsets.ModelViewSet):
    permission_classes = ( IsAuthenticatedOrReadOnly, )
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer

class sample_carouselViewSet(viewsets.ModelViewSet):
    permission_classes = ( IsAuthenticatedOrReadOnly, )
    queryset = SampleCarouselServices.objects.all()
    serializer_class = LandingPagecarouselSerializer