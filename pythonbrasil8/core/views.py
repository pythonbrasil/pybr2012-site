# -*- coding: utf-8 -*-
from django.views.generic import ListView
from django.views.generic import TemplateView

#from mittun.sponsors.views import SponsorsView
from mittun.sponsors.models import Sponsor, Category
from mittun.events.models import Event


class CustomSponsorsView(ListView):

    template_name = "sponsors.html"
    model = Sponsor

    def get_context_data(self, **kwargs):
        context = super(CustomSponsorsView, self).get_context_data(**kwargs)
        context['sponsors_categories'] = Category.objects.all()
        return context


class Home(ListView):
    model = Sponsor
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        context['event'] = Event.objects.all()[0]
        return context


class VenueView(TemplateView):
    template_name = 'venue.html'


class SponsorsInfoView(TemplateView):
    template_name = 'sponsors_info.html'


class SuccessfulPreRegistration(TemplateView):
    template_name = 'success_pre_registration.html'
