from django.views.generic import View
from django.http import HttpResponse

from pythonbrasil8.subscription.models import Subscription


class SubscriptionView(View):
    def post(self, request, *args, **kwargs):
        if request.user:
            Subscription.objects.create(
                status='pending',
                type='talk',
                user=request.user,
            )
            return HttpResponse("subscription created with success!")
        return HttpResponse("you should be logged in.", status=500)
