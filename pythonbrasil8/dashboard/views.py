# -*- coding: utf-8 -*-
from django.contrib import messages
from django.utils.translation import ugettext
from django.views.generic import ListView, TemplateView, UpdateView

from pythonbrasil8.core.views import LoginRequiredMixin
from pythonbrasil8.dashboard.forms import ProfileForm, SpeakerProfileForm
from pythonbrasil8.dashboard.models import AccountProfile
from pythonbrasil8.schedule.models import Session


class DashBoardView(LoginRequiredMixin, TemplateView):
    pass


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/profile.html'
    model = AccountProfile
    success_url = "/dashboard/"

    def get(self, *args, **kwargs):
        self.kwargs['pk'] = self.request.user.get_profile().id
        return super(ProfileView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        self.kwargs['pk'] = self.request.user.get_profile().id
        r = super(ProfileView, self).post(*args, **kwargs)
        if 300 < r.status_code < 400:
            messages.success(self.request, ugettext(u"Profile successfully updated."), fail_silently=True)
        return r

    def get_form_class(self):
        if self.object.type == "Speaker":
            return SpeakerProfileForm
        return ProfileForm


class IndexView(DashBoardView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['sessions'] = Session.objects.filter(speakers=self.request.user)
        return context


class SessionsView(LoginRequiredMixin, ListView):
    context_object_name = u"sessions"
    template_name = u"dashboard/sessions.html"

    def get_queryset(self):
        return Session.objects.filter(speakers=self.request.user)
