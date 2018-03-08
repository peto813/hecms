from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
import os
#from django.utils.deconstruct import deconstructible


content_types = {
	'pdf' : 'application/pdf',
	'jpg' : 'image/jpeg',
	'doc' : 'application/msword',
	'docx' : 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
	'png' : 'image/png',
	'xlsx' : 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
	'xls' : 'application/excel'
}

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

def validate_positive_num(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s value is not positive'),
            params={'value': value},
        )

def valid_extensions(value):
	try:
		content_type = str(value.file.content_type)
	except:
		content_type = None
	if content_type:
		valid_extensions = ['pdf','jpg','doc','docx','png','xlsx','xls' ]
		value_found = False
		for extension in valid_extensions:
			if content_types[extension] == content_type:
				value_found = True
		if value_found == False:
			raise ValidationError(u'Unsupported file extension.')


def max_20BMfile_size(value):
	file_size = value.size
	if file_size > 20000000:
		raise ValidationError(u'File too Large')



# def min_length(value):
# 	print value
	# def length_validation(value):
	# 		if len(str(value)) < int(length):
	# 			raise ValidationError(u'Min %s Characters' %(length))
	# length_validation()


def min_length8(value):
	if len(str(value)) < 8:
		raise ValidationError(u'Min 8 Characters')




def Integer_Only(value):
	try:
		value = int(value)
	except:
		raise ValidationError(u'Only numbers allowed')


