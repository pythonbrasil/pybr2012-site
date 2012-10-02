# -*- coding: utf-8 -*-
from django import http, shortcuts
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template import response
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, View

from pythonbrasil8.core.views import LoginRequiredMixin
from pythonbrasil8.schedule.forms import SessionForm
from pythonbrasil8.schedule.models import Session, Track


class SubscribeView(LoginRequiredMixin, CreateView):
    form_class = SessionForm
    template_name = "schedule/subscribe.html"

    def get_success_url(self):
        return reverse("dashboard-index")

    def get_extra_speakers(self):
        es = self.request.POST.getlist("extra_speakers")
        return User.objects.filter(Q(username__in=es) | Q(email__in=es))

    def form_valid(self, form):
        r = super(SubscribeView, self).form_valid(form)
        spkrs = [self.request.user]
        spkrs.extend(self.get_extra_speakers())
        self.object.speakers = spkrs
        self.object.save()
        return r

    def get(self, request, *args, **kwargs):
        r = super(SubscribeView, self).get(request, *args, **kwargs)
        r.context_data["tracks"] = Track.objects.all()
        return r

    def post(self, request, *args, **kwargs):
        r = super(SubscribeView, self).post(request, *args, **kwargs)
        if isinstance(r, http.HttpResponseRedirect):
            messages.success(request, _("Session successfully submitted!"), fail_silently=True)
        else:
            r.context_data["extra_speakers"] = self.request.POST.getlist("extra_speakers")
        return r


class EditSessionView(LoginRequiredMixin, View):
    form_class = SessionForm
    template_name = "schedule/edit-session.html"

    def get(self, request, id):
        session = shortcuts.get_object_or_404(Session, pk=id, speakers=request.user)
        form = self.form_class(instance=session)
        tracks = Track.objects.all()
        return response.TemplateResponse(request, self.template_name, {"session": session, "form": form, "tracks": tracks})

    def post(self, request, id):
        session = shortcuts.get_object_or_404(Session, pk=id, speakers=request.user)
        form = self.form_class(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, _("Session successfully updated!"), fail_silently=True)
            return http.HttpResponseRedirect(reverse("dashboard-sessions"))
        tracks = Track.objects.all()
        return response.TemplateResponse(request, self.template_name, {"session": session, "form": form, "tracks": tracks})


class DeleteSessionView(LoginRequiredMixin, View):

    def get(self, request, id):
        session = shortcuts.get_object_or_404(Session, pk=id, speakers=request.user)
        session.delete()
        messages.success(request, _("Session successfully deleted!"), fail_silently=True)
        return http.HttpResponseRedirect(reverse("dashboard-sessions"))


class FinishedProposalsView(LoginRequiredMixin, View):
    template_name = u"schedule/finished_proposals.html"

    def get(self, request):
        return response.TemplateResponse(request, self.template_name)
