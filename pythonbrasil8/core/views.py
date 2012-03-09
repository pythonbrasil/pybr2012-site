from django.views.generic import ListView
from mittun.sponsors.models import Sponsor


class Home(ListView):
    model = Sponsor
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        return context
