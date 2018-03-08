# -*- coding: utf-8 -*-

# encoding=utf8  
import sys , json

reload(sys)  
sys.setdefaultencoding('utf8')

from userapp.models import *
from django.shortcuts import render, render_to_response
import paypalrestsdk
from itertools import chain
import paypal
from serializers import (

    Auction_ProductsSerializer,
    AuctionsSerializer,
    ChangePasswordSerializer,
    deleteProductsSerializer,
    LogisticsSerializer,
    MaintenanceSerializer,
    updateEmailSerializer,
    UserDetailsViewSerializer, 
    UserProfilePictureSerializer,
    UserSerializer,
    #ConfirmEmailSerializer,
    EditProductsSerializer,
    ServiceSerializer,
    Inspection_TypeSerializer,
    InspectionSerializer,
    PaypalSerializer,
    )
from django.db.models import Q

from permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from django.contrib.auth.models import User
from django.conf import settings
from django.views.generic import TemplateView
    #DJANGO FRAMEWORK
from django.http import Http404

        #REST FRAMEWORK
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
#from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
#REST AUTH
from rest_auth.views import LoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_auth.registration.views import SocialLoginView

#ALLAUTH DEPENDENCIES
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from allauth.account.models import EmailAddress
##############TWIITER AUTH#################
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs



# Create your views here.
def index(request):
    if ('oauth_token' and 'oauth_verifier') in str(request.GET):
        try:
            #if ('oauth_token' and 'oauth_verifier') in str(request.GET):
            data = {}
            oauth_verifier = request.GET.get('oauth_verifier')
            oauth_token = request.GET.get('oauth_token')
            resource_owner_key = request.session['resource_owner_key']
            if resource_owner_key == oauth_token:
                oauth = OAuth1(settings.CONSUMER_KEY,
                               client_secret=settings.CONSUMER_SECRET,
                               resource_owner_key=resource_owner_key,
                               resource_owner_secret=request.session['resource_owner_secret'],
                               verifier=oauth_verifier)

                del request.session['resource_owner_key']
                del request.session['resource_owner_secret']
                r = requests.post(url=settings.ACCESS_TOKEN_URL, auth=oauth)
                credentials = parse_qs(r.content)
                data['token_secret'] = credentials['oauth_token_secret']
                data['access_token'] = credentials['oauth_token']
                r = requests.post('http://%s/rest-auth/twitter/' %(request.get_host()), data=data ).json() #auth=('user', 'pass')
                
                context = {
                    'title':'HM-Ship | Welcome',
                    'tokenDict' : json.dumps(r)
                }
                
                return render(request, 'index.html', context)
        except:
            pass
    context = {
    'title':'HM-Ship | Welcome'
        #'facebook_app_id' : settings.FACEBOOK_APP_ID
       }
    return render(request, 'index.html', context)

def Paypal_Return_View(request):
    if request.method == 'GET':
        data = request.GET.copy()
        payment = paypalrestsdk.Payment.find(data['paymentId'])
        payment.execute({"payer_id": data['PayerID']})
        print payment
        #print data
        # url  = str('https://api.sandbox.paypal.com/v1/payments/%s/execute' %( data['paymentId'] ))
        # token = str('Bearer %s' %( data['token'] ))
        # headers = { 'Authorization': token }
        # payload = {'payer_id' : data['PayerID']}
        # r = requests.post( url, data = payload, headers = headers)
        # print r, r.content
        #credentials = parse_qs(r.content)
        #print credentials

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
#                 print 1
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


## EXPERIMENTAL

class confirmEmailView(TemplateView):
    template_name = "email_confirm.html"
    # queryset = EmailConfirmation.objects.all()
    # serializer_class = ConfirmEmailSerializer
    def get_context_data(self, **kwargs):
        if kwargs['key']:
            r = requests.post('http://%s/rest-auth/registration/verify-email/' %( self.request.get_host()), data = kwargs )
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

class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter

class TwittterOauth(APIView):
    renderer_classes = (JSONRenderer, )
    def get(self, request):
        # Request oauth token
        oauth = OAuth1(settings.CONSUMER_KEY, client_secret=settings.CONSUMER_SECRET)
        r = requests.post(url=settings.REQUEST_TOKEN_URL, auth=oauth)
        credentials = parse_qs(r.content)
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]

        #DJANGO SESSION STORES CREDENTIALS
        request.session['resource_owner_key'] = resource_owner_key
        request.session['resource_owner_secret'] = resource_owner_secret

        # Authorize url
        authorize_url = settings.AUTHORIZE_URL + resource_owner_key

        return Response(authorize_url)

class GoogleLogin(SocialLoginView):
    #serializer_class = TwitterLoginSerializer
    adapter_class = GoogleOAuth2Adapter


class AuctionsViewSet(viewsets.ModelViewSet):
    queryset = Auctions.objects.filter(auction_open = True)
    serializer_class = AuctionsSerializer
    permission_classes = ( IsAuthenticated, )

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = AuctionsSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)


    #queryset = self.get_queryset()
    #serializer = UserSerializer(queryset, many=True)




class AuctionsProductsViewSet(viewsets.ModelViewSet, GenericAPIView):
    queryset = Auction_Products.objects.all()
    serializer_class = Auction_ProductsSerializer
    permission_classes = ( 
        IsAuthenticated, 
        #AllowAny,
        )

    def get_object(self, pk):
        try:
            return Auction_Products.objects.get(pk=pk)
        except Auction_Products.DoesNotExist:
            raise Http404


    def get_serializer_context(self):
        return { 'request': self.request }

    def get_queryset(self):
        queryset_list = self.queryset.filter(user = self.request.user)
        
        query = self.request.GET.get('q')

        if query == 'logistics':
            queryset_list = queryset_list.exclude( services__logistics__isnull = False )

        elif query == 'inspections':
            queryset_list = queryset_list.exclude( services__inspections__isnull = False )
            
        elif query == 'maintenance':
            queryset_list = queryset_list.exclude( services__maintenance__isnull = False )
        return queryset_list

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
            return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )


class EditProductsViewSet(AuctionsProductsViewSet):
    serializer_class = EditProductsSerializer
    def update(self, request, pk, format=None):
        snippet = self.get_object(pk)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#view that approves or rejects service quotes
class ServicesViewSet(AuctionsProductsViewSet):
    #queryset = Services.objects.all()
    permission_classes = ( 
        IsAuthenticated, 
        #AllowAny,
        )

    def get_object(self, pk):
        try:
            return Services.objects.get(pk=pk)
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




class CreateOrUpdatePicView(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = UserProfilePictureSerializer
    model = UserProfile

    permission_classes = (
        IsAuthenticated,
        #AllowAny,
        )

    def get(self, request):
        serializer = UserProfilePictureSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserProfilePictureSerializer( data = request.data )
        if serializer.is_valid():
            cd =  serializer.validated_data
            try:
                obj = UserProfile.objects.get(user=request.user)
                obj.company_name = cd.get('company_name')
                obj.profile_picture = cd.get('profile_picture')

            except UserProfile.DoesNotExist:
                obj = UserProfile( user = request.user, company_name=cd.get('company_name'), profile_picture = cd.get('profile_picture') )
            
            obj.save()
            serializer = UserProfilePictureSerializer(obj)
            return Response( serializer.data )
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format = None):
        try:
            user_obj = UserProfile.objects.get(user = request.user)
            user_obj.profile_picture = None
            user_obj.save()
            serializer = UserProfilePictureSerializer(user_obj)
            return Response(serializer.data)
        except:
            return Response("No Picture object", status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

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

class deleteProductsView(viewsets.ModelViewSet):
    queryset = Auction_Products.objects.all()
    serializer_class = deleteProductsSerializer
    permission_classes = (  
        AllowAny, 
        #IsAuthenticated, 
        #IsOwnerOrReadOnly,
    )
    def create(self, request):
        serializer = deleteProductsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogisticsViewSet(viewsets.ModelViewSet):
    queryset = Logistics.objects.all()
    serializer_class = LogisticsSerializer
    permission_classes = (  
        AllowAny,
        #IsAuthenticated, 
        #IsOwnerOrReadOnly,
    )
    # def get_object(self, pk ):
    #     print pk
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
        #     #print serializer.validated_data
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # else:
        #     print serializer.errors
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
        #AllowAny, 
        IsAuthenticated, 
        #IsOwnerOrReadOnly,
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
        #IsOwnerOrReadOnly,
    )

class InspectionsViewSet(viewsets.ModelViewSet):
    queryset = Inspections.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
        #IsOwnerOrReadOnly,
    )

    # def list(self, request):
    #     serializer = Auction_ProductsSerializer( 
    #         Auction_Products.objects.filter(user = request.user).filter(maintenance__isnull = True), many= True )
    #     return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data= request.data, context = {'request': request}, method = 'create')
        print request.data
        if serializer.is_valid():
            serializer.save()
            return Response('Success', status=status.HTTP_200_OK)
        else: 
            print serializer.errors  
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



class OrderBookViewSet( viewsets.ModelViewSet ):
    queryset = Services.objects.all( )
    serializer_class = ServiceSerializer
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
        #IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        services = Services.objects.filter(user = self.request.user)
        return services

    def list(self, request):
        serializer = self.get_serializer( self.get_queryset(), many= True )
        return Response(serializer.data)

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
        #IsOwnerOrReadOnly,
    )
    renderer_classes = (JSONRenderer, )
    # def get_queryset(self):
    #     queryset_list = Services.objects.filter(user = self.request.user)
    #     return queryset_list

    def post(self, request, format=None):
        #queryset = self.get_queryset()
        # data  = request.data.copy()
        # data['service_id_list'] = [99]
        serializer = PaypalSerializer( data = request.data)
        if serializer.is_valid():
            #print serializer.validated_data
            payment = paypal.create_payment( request  , serializer.validated_data['service_id_list'])
            #serializer.save()service_id_list
            #print payment
            for link in payment.links:
                if link.rel == 'approval_url':
                    return Response(link.href, status=status.HTTP_200_OK)
            #print type(payment)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        print serializer.errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



#GETS THE USER DETAILS WHEN LOGIN
class UserDetailsView(APIView):
    permission_classes = (  
        #AllowAny, 
        IsAuthenticated, 
        #IsOwnerOrReadOnly,
    )
    lookup_field = 'id'
    def get(self, request):
        serializer = UserDetailsViewSerializer(request.user)

        return Response(serializer.data)

    #USE THIS TO UPDATE USER MODEL DETAILS SUCH AS FIRST, LAST, AND COMPANY NAME
    def put(self, request ):
        #snippet = self.get(request)
  #       permission_classes = (  
        #   #AllowAny, 
        #   IsAuthenticated, 
        #   #IsOwnerOrReadOnly,
        # )

        #data['username'] = request.user.username
        serializer = UserDetailsViewSerializer(request.user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk = None):
        instance = self.get_object(pk)
        serializer = ServiceSerializer(instance, data = request.data, partial=True, context = {'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class upDateEmailView(APIView):
    def put(self, request ):
        serializer = updateEmailSerializer(instance = request.user, data = request.data, context = {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response("Success", status=status.HTTP_200_OK)
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

            #LOGIN TEST FOR OBTAINING TOKEN
#curl -X POST -d "email=peto813@gmail.com&password=ou63ut14" http://127.0.0.1:8000/rest-auth/login/
    #logout
#curl  POST  http://127.0.0.1:8000/rest-auth/logout/


        #TOKEN
#Token 4de3202c311f39fc87eb86cd7fb2ea41bc1ffa13


    #ACCESS PROTECTED API ROUTES(EXAMPLE)

        #WITH CREDENTIAL
#curl -H "Authorization: Token 4de3202c311f39fc87eb86cd7fb2ea41bc1ffa13" http://127.0.0.1:8000/api/userdetails/1

        #WITHOUT CREDENTIAL
#curl http://peto813.ddns.net:9000/api/userdetails/1/



#curl -X POST -H "Content-Type: application/json" 
#-d '{ "email":"peto813@gmail.com" }' http://127.0.0.1:8000/userdetails/(?P<pk>
#Refresh Token


# Create your views here.
# def join(request):
#   #carousel_images = 
#   context = {
#       'title':'HM-Ship | Join'
#   }

#   return render(request, 'join.html', context)