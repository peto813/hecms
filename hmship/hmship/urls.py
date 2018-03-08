"""hmship URL Configuration
 
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from rest_framework import routers
from django.contrib import admin
from django.conf import settings
from userapp import views
from django.conf.urls.static import static
from allauth.account.views import confirm_email

from userapp.views import (

    FacebookLogin,
    TwitterLogin,
    UserDetailsView,
    ChangePasswordView,
    CreateOrUpdatePicView,
    GoogleLogin,
    LogisticsViewSet,
    AuctionsViewSet,
    AuctionsProductsViewSet,
    Bank_AccountsViewSet,
    MaintenanceViewSet,
    #OrderBookViewSet,
    TwitterOauth,
    upDateEmailView,
    confirmEmailView,
    #AboutView,
    EditProductsViewSet,
    deleteProductsViewSet,
    UserViewSet,
    InspectionsViewSet,
    InspectionTypesViewSet,
    PaymentsViewSet,
    PaypalView,
    Paypal_Return_View,
    ServicesViewSet,
    ContactUsView,
    fill_inspection,
    InspectionReportViewSet,
    inspection_report_success,
    LandingPageView,
    InspectionCarouselView,
    LogisticsCarouselViewSet,
    CustomLoginView,
    customPasswordResetView,
    sample_carouselViewSet,
    InspectionCarouselSampleView,
    )


router = routers.DefaultRouter()

router.register( r'deleteauctionproducts', views.deleteProductsViewSet, 'deleteproducts' )#PERMISSIONS SET IN SERIALIZER
router.register( r'auctions', views.AuctionsViewSet, 'auctions' )#PERMISSIONS SET
router.register( r'logistics', views.LogisticsViewSet,'logistics' )#PERMISSIONS SET
router.register( r'maintenance', views.MaintenanceViewSet )#PERMISSIONS SET
router.register( r'auctionproducts', views.AuctionsProductsViewSet, 'auctionproducts' )#PERMISSIONS SET
router.register(r'users', UserViewSet)#PERMISSIONS SET
router.register(r'editproducts', EditProductsViewSet)#PERMISSIONS SET
router.register(r'inspectiontypes', InspectionTypesViewSet)
router.register(r'inspection', InspectionsViewSet)#PERMISSIONS SET
router.register(r'services', ServicesViewSet)#PERMISSIONS SET
router.register(r'userprofile', UserDetailsView, 'userprofile')#PERMISSIONS SET
router.register(r'bankaccounts', Bank_AccountsViewSet, 'bankaccounts')#PERMISSIONS SET
router.register(r'payments', PaymentsViewSet, 'payments')#PERMISSIONS SET
router.register(r'inspectionreport', InspectionReportViewSet, 'inspectionreport')#PERMISSIONS SET
router.register(r'logistics_carousel', LogisticsCarouselViewSet, 'logistics_carousel')#PERMISSIONS SET
router.register(r'sample_carousel', sample_carouselViewSet, 'sample_carousel')#PERMISSIONS SET
urlpatterns = [
    
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/fill_inspection/(?P<inspection_id>[0-9]+)/$', fill_inspection, name='fill_inspection'),
    url(r'^admin/inspection_success/$', inspection_report_success, name='inspection_report_success'),
    url(r'^$', views.index, name = 'index'),
    #url(r'^twitter_login/$', views.twitter_login.as_view(), name='twitter_login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework')),

    #REST FRAMEWORK URLS
    url(r'^rest-auth/password/reset/$', customPasswordResetView.as_view(), name='rest_password_reset'),
    url(r'^rest-auth/login/$', CustomLoginView.as_view(), name='rest_login'),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', confirmEmailView.as_view(), name="account_confirm_email"),
    url(r'^rest-auth/', include('rest_auth.urls')), 
    #DJANGO URLS
    url(r'^', include('django.contrib.auth.urls')),

    #ALLAUTH URLS
    url(r'^accounts/', include('allauth.urls')),

    #REST-AUTH URL OVERRRIDE
    #url(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email, name="account_confirm_email"),
    #url(r'^rest-auth/registration/verify-email/$', confirm_email, name="account_confirm_email"),

    #REST AUTH URLS
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/twitter/$', TwitterLogin.as_view(), name='twitter_login'),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),

    #API URLS
    #url(r'^api/userdetails/$', UserDetailsView.as_view(), name='userdetails'),
    url(r'^api/changepassword/$', ChangePasswordView.as_view(), name='changepassword'),#PERMISSIONS SET
    url(r'^api/contactus/$', views.ContactUsView.as_view(), name='contact_us'),
    url(r'^api/profileimage/$', CreateOrUpdatePicView.as_view(), name='profileimage'),
    url(r'^api/twitteroauth/$', TwitterOauth.as_view(), name='twitteroauth'),
    url(r'^api/updatemail/$', upDateEmailView.as_view(), name='updatemail'),
    url(r'^api/paypal/$', PaypalView.as_view(), name='updatemail'),
    url(r'^paypal/return_url/$', views.Paypal_Return_View, name='paypal_return_url'),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^api/landing_page_images/$', LandingPageView.as_view(), name='landing_page_images'),
    url(r'^api/inspection_carousel/(?P<service>[0-9]+)/$', InspectionCarouselView.as_view(), name='inspection_carousel'),
    url(r'^api/inspection_carousel_sample_detail/(?P<service>[0-9]+)/$', InspectionCarouselSampleView.as_view(), name='landing_page_sample_images'),
    #url(r'^api/auctionproducts/delete/$', deleteProductsView.as_view(), name='deleteauctionproducts'),
    #url(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/$', confirm_email, name="account_confirm_email"), 
    #url(r'^api/updatemail/$', upDateEmailView.as_view(), name='updatemail'),
    #rest-auth/registration/ ^account-confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
    #url(r'^rest-auth/registration/account-confirm-email/(?P<key>\w+)/$', AboutView.as_view(), name="account_confirm_email")

    
    #url(r'^rest-auth/registration/verify-email/(?P<key>\w+)/$', confirmEmailView.as_view(), name="account_confirm_email"),
    #url(r'^api/logistics/$', LogisticsView.as_view(), name='logistics'),
    #url(r'^api/test/$', Test.as_view({'get': 'list'}), name='test'),
    #url(r'^rest-auth/google/$', TwitterLogin.as_view(), name='google_login'),
    #url(r'^join/$', views.join, name='join'),
    #url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# from django.conf.urls.static import static
# from django.conf.urls import include, url


# #from allauth.account.views import SignupView, password_change
# #from allauth.account import views as allauthviews



# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^$', views.index, name='index')
# ]
