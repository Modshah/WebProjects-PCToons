from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Product, User, tags
from django.utils.translation import ugettext_lazy


class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('PareshToon')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('My administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('PareshToon')


class ImageAdmin(admin.ModelAdmin):
    list_filter = [field.name for field in Product._meta.get_fields()]
    #list_display = [field.name for field in Product._meta.get_fields()]
    search_fields = ['title', 'id', 'image']


admin_site = MyAdminSite()
admin.site.register(Product, ImageAdmin)
admin.site.register(tags)
admin.site.register(User)
