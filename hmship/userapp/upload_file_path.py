import os
def payment_proof_upload_path(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'user_files', str(instance.user.pk), 'payment_proof', filename ))


def quote_upload_path(instance, filename):
    service_type = instance.service_type
    return os.path.join( '%s/%s/%s_quotes/%s' % ( 'user_files', str(instance.user.pk), service_type, filename ))


def auction_products(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'user_files', str(instance.user.pk), 'auction_products', filename ))


def upload_profile_picture(instance, filename):
    return os.path.join( '%s/%s/%s/%s' % ( 'user_files', str(instance.user.pk), 'profile_picture', filename ))


def inspection_item_picture(item, filename):
	#section_name = str(instance.section.name).replace(" ", "")
    return os.path.join( 'admin/inspections/reports/item/%s/%s' % ( str(item.row.description.replace(" ", "_")), filename  ) )

def auction_image(instance, filename):
    return os.path.join( '%s/%s/' % ( 'auctions', filename ))


def logistics_report_upload(instance, filename):
    return os.path.join( '%s/%s/' % ( 'logistics', filename ))

def maintenance_report_upload(instance, filename):
    return os.path.join( '%s/%s/' % ( 'logistics', filename ))

def report_upload_path(instance, filename):
    return os.path.join( '%s/%s/' % ( 'logistics', filename ))