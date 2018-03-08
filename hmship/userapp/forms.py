from .models import *
from django.core.exceptions import ValidationError
from django import  forms
from django.contrib.auth.forms import PasswordResetForm
#from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _

UserModel = get_user_model()

class customPasswordResetForm(PasswordResetForm):
    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override

            context = {
                'email': email,
                'domain': domain.replace('https://' if use_https else 'http://', '').strip('/'),
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            if extra_email_context is not None:
                context.update(extra_email_context)

            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )





class CarouselItemsForm(forms.ModelForm):
    image= forms.ImageField(required = True)
    class Meta:
        model = Carousel_Image
        fields = ['image', 'text', 'item_type', 'service' ]

    def clean_image(self):
        image = self.cleaned_data['image']
        #from django.core.files.images import get_image_dimensions
        #width, height = get_image_dimensions(image)
        #print width, height   
        # if image.size > 50000:
        #     raise forms.ValidationError('Imagen no puede ser mas de 50kb')

        return image



class Inspection_Row_Form(forms.ModelForm):
    class Meta:
        model = Inspection_Report_Rows
        fields = ['row', 'rating', 'details', 'item_picture' ]

    # def clean(self):
    #     cleaned_data = super(Inspection_Row_Form, self).clean()
    #     item_picture = cleaned_data.get( 'item_picture', None )
    #     rating= cleaned_data.get( 'rating', None )
    #     details= cleaned_data.get( 'details', None )

    #     if details:
    #         if not rating:
    #             self.add_error('rating', "Add a rating")

    #         elif not item_picture:
    #             self.add_error('item_picture', "Add picture")

    #     if rating:
    #         if not details:
    #             self.add_error('details', "Add details")
    #         elif not item_picture:
    #             self.add_error('item_picture', "Add picture")  

class Inspection_ReportForm(forms.ModelForm):
    report = forms.FileField(required = False)
    class Meta:
        model = Services
        fields = '__all__'

    def clean_report(self):
        report = self.cleaned_data['report']
        try:
            if report:
                file_type = report.content_type.split('/')[0]

                if len(report.name.split('.')) == 1:
                    raise forms.ValidationError(_('File type is not supported'))

                if file_type =='pdf':
                    if report._size > 10000000:
                        raise forms.ValidationError(_('Please keep filesize under %s.') % (str(10000000)))
                else:
                    raise forms.ValidationError(_('File type is not supported'))
        except:
            pass

        return report

class SampleReportForm(forms.ModelForm):
    inspection = forms.ModelChoiceField(queryset=SampleCarouselServices.objects.filter(object_type='Inspections'), empty_label="Sample inspections", help_text='These are the created sample inspections')
    class Meta:
        model = SampleInspectionReportRow
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(SampleReportForm, self).__init__(*args, **kwargs)
    #     self.fields['inpection'].queryset = SampleInspectionReportRow.objects.filter(inspection)