from django.views.generic import ListView
from django.views.generic import TemplateView

from mittun.sponsors.models import Sponsor

from core.models import Home


class Home(ListView):
    model = Home
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        return context


class VenueView(TemplateView):
    template_name = 'venue.html'
