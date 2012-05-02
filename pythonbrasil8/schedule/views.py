from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from pythonbrasil8.schedule.forms import SessionForm


def session_subscribe_view(request):
    form = SessionForm(request.POST or {})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/dashboard/")

    context = {
        "form": SessionForm(request.POST),
    }
    return TemplateResponse(request, "schedule/subscribe.html", context)
