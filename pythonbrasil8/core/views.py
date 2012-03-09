from django.views.generic import ListView
from django.views.generic import TemplateView

from mittun.sponsors.models import Sponsor
from mittun.events.models import Event


class Home(ListView):
    model = Sponsor
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        context['event'] = Event.objects.all()[0]
        return context


class VenueView(TemplateView):
    template_name = 'venue.html'
