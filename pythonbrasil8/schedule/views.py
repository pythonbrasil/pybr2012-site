from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from pythonbrasil8.schedule.forms import SessionForm


class SubscribeView(CreateView):
    form_class = SessionForm
    template_name = 'schedule/subscribe.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SubscribeView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard-index')
