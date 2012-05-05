# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from pythonbrasil8.schedule.models import Session
from pythonbrasil8.dashboard.forms import ProfileForm


class DashBoardView(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DashBoardView, self).dispatch(*args, **kwargs)


class ProfileView(DashBoardView):
    template_name = 'dashboard/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['form'] = ProfileForm()
        return context

class IndexView(DashBoardView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['sessions'] = Session.objects.filter(speakers=self.request.user)
        return context

