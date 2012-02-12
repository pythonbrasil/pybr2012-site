from django.views.generic import ListView
from core.models import Site

class Index(ListView):
    model = Site
    template_name = 'index.html'
