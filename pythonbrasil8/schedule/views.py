from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from pythonbrasil8.schedule.forms import SessionForm


@login_required
def session_subscribe_view(request):
    form = SessionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/dashboard/")

    context = {
        "form": form,
    }
    return TemplateResponse(request, "schedule/subscribe.html", context)
