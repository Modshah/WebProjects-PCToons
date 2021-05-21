"""pcadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.contrib.auth.models import User
from padmin.models import Image_Upload, tags, subscribers,Products
from rest_framework import routers, serializers, viewsets
from padmin.views import (
    CreateCheckoutSessionView,
    ProductsLandingPageView,
    SuccessView,
    CancelView,
    stripe_webhook,
    StripeIntentView
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image_Upload
        fields = [field.name for field in Image_Upload._meta.get_fields()]

class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = subscribers
        fields = [field.name for field in subscribers._meta.get_fields()]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = Image_Upload.objects.all()
    serializer_class = UserSerializer


class SubscriberSet(viewsets.ModelViewSet):
    queryset = subscribers.objects.all()
    serializer_class = SubscriberSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
router.register(r'Image_Upload', UserViewSet)
router.register(r'subscribers', SubscriberSet)



urlpatterns = [

    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('create-payment-intent/<pk>/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('payment/<pk>/', ProductsLandingPageView.as_view(), name='landing-page'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
