# -*- coding: utf-8 -*-
from django import http
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views.generic import CreateView

from pythonbrasil8.core.views import LoginRequiredMixin
from pythonbrasil8.schedule.forms import SessionForm


class SubscribeView(LoginRequiredMixin, CreateView):
    form_class = SessionForm
    template_name = 'schedule/subscribe.html'

    def get_success_url(self):
        return reverse('dashboard-index')

    def get_extra_speakers(self):
        es = self.request.POST.get("extra_speakers", [])
        if isinstance(es, basestring):
            es = [es]
        return User.objects.filter(Q(username__in=es) | Q(email__in=es))

    def form_valid(self, form):
        r = super(SubscribeView, self).form_valid(form)
        spkrs = [self.request.user]
        spkrs.extend(self.get_extra_speakers())
        self.object.speakers = spkrs
        self.object.save()
        return r

    def post(self, request, *args, **kwargs):
        r = super(SubscribeView, self).post(request, *args, **kwargs)
        if isinstance(r, http.HttpResponseRedirect):
            messages.success(request, _("Session successfully submitted!"), fail_silently=True)
        return r
