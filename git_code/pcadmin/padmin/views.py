from django.shortcuts import render
import json
import stripe
from .models import Image_Upload, User, tags, subscribers, Products, Image_Watermark
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"



class ProductsLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        Products_id = self.kwargs["pk"]
        Product = Image_Watermark.objects.get(id=Products_id)
        context = super(ProductsLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "Product": Product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context


# noinspection PyUnresolvedReferences
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        Products_id = self.kwargs["pk"]
        Product = Image_Watermark.objects.get(id=Products_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        ##print("checkoutsession")
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'INR',
                        'unit_amount': '200',
                        'product_data': {
                            'name': Product.image_name,
                            ##'images': Product.compress_img,
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "Products_id": Product.id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    print("webhook_stripe_Session")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_email = session["customer_details"]["email"]
        Products_id = session["metadata"]["Products_id"]

        Product = Image_Watermark.objects.get(id=Products_id)

        send_mail(
            subject="Here is your Products",
            message=f"Thanks for your purchase. Here is the Products you ordered. The URL is {Product.compress_img}",
            recipient_list=[customer_email],
            from_email="pareshtoondjnago@gmail.com"
        )

        # TODO - decide whether you want to send the file or the URL

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']
        print('hello I am succesed')

        stripe_customer_id = intent["customer"]
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        Products_id = intent["metadata"]["Products_id"]

        Product = Image_Watermark.objects.get(id=Products_id)

        send_mail(
            subject="Here is your Products",
            message=f"Thanks for your purchase. Here is the Products you ordered. The URL is {Product.compress_img}",
            recipient_list=['mightygrv@gmail.com'],
            from_email="pareshtoondjnago@gmail.com"
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            Products_id = self.kwargs["pk"]
            Product = Image_Watermark.objects.get(id=Products_id)
            intent = stripe.PaymentIntent.create(
                description='Software development services',
                shipping={
                    'name': 'Jenny Rosen',
                    'address': {
                        'line1': '510 Townsend St',
                        'postal_code': '110059',
                        'city': 'New Delhi',
                        'state': 'New Delhi',
                        'country': 'India',
                    },
                },
                amount=200,
                currency='inr',
                customer=customer['id'],
                metadata={
                    "Products_id": Product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
# Create your views here.
