from django.template.response import TemplateResponse


def session_subscribe_view(request):
    return TemplateResponse(request, "schedule/subscribe.html", {})
