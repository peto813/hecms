# -*- coding: utf-8 -*-

# encoding=utf8  
import django_filters
from models import *
from django.db.models import Q
from django.db import models as django_models
import models
#http://hecms.com/api/auctionproducts?category=clothing&max_price=10.00
#http://hecms.com/api/auctionproducts?lot_number=123465

class Services_Filter(django_filters.FilterSet):
    search_param = django_filters.CharFilter( method = 'my_custom_filter' )
    #timestamp_gte = django_filters.DateTimeFilter( name = "created", lookup_expr = 'gte' )
    #timestamp_lte = django_filters.DateTimeFilter( name = "created", lookup_expr = 'lte' )
    #resolved = django_filters.DateTimeFilter( name = "timestamp", lookup_expr = 'lte' )
    timestamp_gte = django_filters.IsoDateTimeFilter(name = "created", lookup_expr = 'gte')
    timestamp_lte = django_filters.IsoDateTimeFilter(name = "created", lookup_expr = 'lte')
    class Meta:
        model = Services
        fields = [ 'search_param', 'created' ]
        #fields = {"search_param": ['iexact', 'icontains', 'in', 'startswith']}

        # filter_overrides = {
        # 	django_models.DateTimeField: {
        # 	'filter_class': django_filters.IsoDateTimeFilter
        # 	}

        # }

    def my_custom_filter( self, queryset, name, value ):
    	try:
    		return queryset.filter(
    			id = value
    			)
    	except:
    		return queryset.filter(
    			service_type = value.title()
    			)



class Products_Filter(django_filters.FilterSet):
    timestamp_gte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'gte' )
    timestamp_lte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'lte' )
    search_param = django_filters.CharFilter( method = 'my_custom_filter' )
    has_open_process = django_filters.CharFilter( name = 'services__has_open_process', lookup_expr = 'iexact' )
    lacks_service_type = django_filters.CharFilter( name = 'services__service_type', lookup_expr = 'exact',exclude = True )
    #user = django_filters.NumberFilter( name = 'services__service_type', lookup_expr = 'exact', exclude = True )
    class Meta:
        model = Auction_Products
        fields = ['search_param', 'created', 'has_open_process', 'lacks_service_type', 'user']

    # def has_logistics(self, queryset, name, value):

    #     return queryset

    def my_custom_filter(self, queryset, name, value):
    	try:
    		products_query = queryset.filter(auction__host = value.lower())
    		if products_query.exists():
    			return products_query
    		raise Exception('No payment_type found')
    	except:
    		pass

    	try:
    		products_query = queryset.filter(lot_number = value)
    		if products_query.exists():
    			return products_query
    		raise Exception('No lot_number found')
    	except:
    		pass

    	return []


class AuctionFilter(django_filters.FilterSet):
    class Meta:
        model = Auctions
        fields = ['auction_open']


class Payments_Filter(django_filters.FilterSet):
    timestamp_gte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'gte' )
    timestamp_lte = django_filters.IsoDateTimeFilter( name = "created", lookup_expr = 'lte' )
    search_param = django_filters.CharFilter(method='payment_custom_filter')
    class Meta:
        model = Payments
        fields = [ 'created', 'id', 'search_param' ]

    def payment_custom_filter(self, queryset, name, value):
    	
    	try:
    		payment_type_query = queryset.filter(payment_type = value.lower())
    		if payment_type_query.exists():
    			return payment_type_query
    		raise Exception('No payment_type found')
    	except:
    		pass

    	try:
    		payment_type_query = queryset.filter(id = value)
    		if payment_type_query.exists():
    			return payment_type_query
    		raise Exception('No payment_id found')
    	except:
    		pass	
    	# try:
    	# 	if value==''
    	# 	payment_type_query = queryset.filter(payment_approved = value)
    	# 	if payment_type_query.exists():
    	# 		return payment_type_query
    	# 	raise Exception('No payment_type found')
    	# except:
    	# 	return queryset.filter(pk = value)

    	return []