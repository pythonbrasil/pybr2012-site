# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, UpdateView

from pythonbrasil8.schedule.models import Session
from pythonbrasil8.dashboard.forms import ProfileForm
from pythonbrasil8.dashboard.models import AccountProfile
from pythonbrasil8.core.views import LoginRequiredMixin


class DashBoardView(LoginRequiredMixin, TemplateView):
    pass


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/profile.html'
    model = AccountProfile
    form_class = ProfileForm
    success_url = '/dashboard/'

    def get(self, *args, **kwargs):
        self.kwargs['pk'] = self.request.user.get_profile().id
        return super(ProfileView, self).get(*args, **kwargs)


class IndexView(DashBoardView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['sessions'] = Session.objects.filter(speakers=self.request.user)
        return context
