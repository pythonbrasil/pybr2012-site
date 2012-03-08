from django.views.generic import ListView
from mittun.sponsors.models import Sponsor
from mittun.events.models import Event

from core.models import Home


class Home(ListView):
    model = Home
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        context['event'] = Event.objects.all()[0]
        return context
