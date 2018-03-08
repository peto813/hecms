"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'hmship.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name
#from allauth import account as teta
import allauth.socialaccount.models as teta
print dir(teta)
class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        #append a group for "Administration" & "Applications"
        # self.children.append(modules.Group(
        #     _('Group: Administration & Applications'),
        #     column=1,
        #     collapsible=True,
        #     children = [
        #         modules.AppList(
        #             _('Administration'),
        #             column=1,
        #             collapsible=True,
        #             models=('django.contrib.*',),
        #         ),
        #         # modules.AppList(
        #         #     _('Applications'),
        #         #     column=1,
        #         #     css_classes=('collapse closed',),
        #         #     exclude=('django.contrib.*',),
        #         # )
        #     ]
        # ))
        
        # append an app list module for "Applications"
        # self.children.append(modules.AppList(
        #     _('1: Applications'),
        #     collapsible=True,
        #     column=1,
        #     css_classes=('collapse closed grp-closed',),
        #     exclude=('django.contrib.*',),
        #     models=(
        #         'userapp.models.Payments',
        #         #'django.contrib.sites.models.Site',
        #         ),
        # ))
        


        self.children.append(modules.ModelList(
            _('1. : Hecms Admin App'),
            column=1,
            collapsible=True,
            css_classes=('collapse closed grp-closed',),
            models=(
                'userapp.models.Services',
                'userapp.models.Payments',
                'userapp.models.Auctions',
                'userapp.models.Auction_Products',
                'userapp.models.Bank_Accounts',
                'userapp.models.Inspection_Types',
            ),

        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('2. : Administration'),
            column=1,
            collapsible=True,
            css_classes=('collapse closed grp-closed',),
            exclude=(
                'userapp.models.Services',
                'userapp.models.Payments',
                'userapp.models.Auctions',
                'userapp.models.Auction_Products',
                'userapp.models.Bank_Accounts',
                'userapp.models.Maintenance',
                'userapp.models.Inspection_Types',
                'userapp.models.Inspections',
                'userapp.models.Logistics',

            ),
            models=(
                'django.contrib.auth.models.User',
                'userapp.models.Inspection_Types_Sections',
                'userapp.models.Inspection_Types_Sections_Items',
                'userapp.models.Inspection_Reports',
                'userapp.models.Carousel_Image',
                'django.contrib.sites.models.Site',
                'allauth.socialaccount.models.SocialApp',
                'userapp.models.Landing_Page_Images',
                'userapp.models.SampleCarouselServices',
                'userapp.models.SampleInspectionReportRow'
                
                #'userapp.models.UserProfile'
                # 'userapp.models.Inspection_Types',
            )
        ))
        # append another link list module for "support".
        # self.children.append(modules.LinkList(
        #     _('Media Management'),
        #     column=2,
        #     children=[
        #         {
        #             'title': _('FileBrowser'),
        #             'url': '/admin/filebrowser/browse/',
        #             'external': False,
        #         },
        #     ]
        # ))
        
        # append another link list module for "support".
        # self.children.append(modules.LinkList(
        #     _('Support'),
        #     column=2,
        #     children=[
        #         {
        #             'title': _('Django Documentation'),
        #             'url': 'http://docs.djangoproject.com/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Grappelli Documentation'),
        #             'url': 'http://packages.python.org/django-grappelli/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Grappelli Google-Code'),
        #             'url': 'http://code.google.com/p/django-grappelli/',
        #             'external': True,
        #         },
        #     ]
        # ))
        
        # append a feed module
        # self.children.append(modules.Feed(
        #     _('Latest Django News'),
        #     column=2,
        #     feed_url='http://www.djangoproject.com/rss/weblog/',
        #     limit=5
        # ))
        
        # append a recent actions module
        # self.children.append(modules.RecentActions(
        #     _('Recent Actions'),
        #     limit=5,
        #     collapsible=False,
        #     column=3,
        # ))


