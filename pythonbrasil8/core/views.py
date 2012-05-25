# -*- coding: utf-8 -*-
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

#from mittun.sponsors.views import SponsorsView
from mittun.sponsors.models import Sponsor, Category, Job
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

    def sponsor_groups(self):
        groups = []
        sponsors = list(Sponsor.objects.select_related('category').all().order_by('category__priority', 'pk'))

        while sponsors:
            row = sponsors[:6]
            sponsors = sponsors[6:]
            groups.append(row)
        return groups

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['sponsor_groups'] = self.sponsor_groups()
        context['event'] = Event.objects.all()[0]
        return context


class VenueView(TemplateView):
    template_name = 'venue.html'


class SponsorsInfoView(TemplateView):
    template_name = 'sponsors_info.html'


class SuccessfulPreRegistration(TemplateView):
    template_name = 'success_pre_registration.html'


class SponsorsJobsView(ListView):
    template_name = 'sponsors_jobs.html'
    model = Job
    context_object_name = 'jobs'


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
