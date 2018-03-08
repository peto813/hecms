import paypalrestsdk, json, decimal
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from paypalrestsdk import Payment, Invoice
import logging



paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": settings.PAYPAL_CLIENT_ID,
  "client_secret": settings.PAYPAL_CLIENT_SECRET })

def create_payment(request, item_list, tax = None, currency = 'USD'):
	currency = 'USD' if currency == None else str(currency)
	tax = '0' if tax == None else str(tax)
	current_site_domain = (get_current_site(request).domain + reverse('paypal_return_url').lstrip('/'))
	total_due = 0
	services_list = []
	for item in item_list:
		item_quote_price =  decimal.Decimal(item.quote_price)
		total_due += item_quote_price
		description =  getattr(item, str(item.service_type).lower()).description
		service_data = {
	                "name": item.service_type + ' service',
	                "sku": str(item.id),
	                "price": str( item_quote_price ),
	                "currency": str(currency),
	                "quantity": 1,
	                "description":  str(description)
	                #'user': str(request.user.id)
	    }	
		services_list.append( service_data )


	payment = Payment({
	    "intent": "sale",

	    # Payer
	    # A resource representing a Payer that funds a payment
	    # Payment Method as 'paypal'
	    "payer": {
	        "payment_method": "paypal"},

	    # Redirect URLs
	    "redirect_urls": {
	        "return_url": current_site_domain,
	        "cancel_url": get_current_site(request).domain},

	    # Transaction
	    # A transaction defines the contract of a
	    # payment - what is the payment for and who
	    # is fulfilling it.
	    "transactions": [{

	        # ItemList
	        "item_list": {
	            "items": services_list
	                },

	        # Amount
	        # Let's you specify a payment amount.
	        "amount": {
	            "total": str(total_due),
	            "currency": "USD"},
	        "description": "This is the payment transaction description."}]})

	# Create Payment and return status
	if payment.create():
	    return payment
	else:
	    print("Error while creating payment:")
	    print(payment.error)


def create_invoice(email, items = None ):
	invoice = Invoice({
	  'merchant_info': {
	    "email": str(email),
	  },
	  "billing_info": [{
	    "email": str(email)
	  }],
	  "items": [{
      "name": "Widgets",
      "quantity": 20,
      "unit_price": {
        "currency": "USD",
        "value": 2
      }
    }]
	})

	response = invoice.create()
	if response:
		return invoice
