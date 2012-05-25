from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from pythonbrasil8.schedule.forms import SessionForm
from pythonbrasil8.core.views import LoginRequiredMixin


class SubscribeView(LoginRequiredMixin, CreateView):
    form_class = SessionForm
    template_name = 'schedule/subscribe.html'

    def get_success_url(self):
        return reverse('dashboard-index')
