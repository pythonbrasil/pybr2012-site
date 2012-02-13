from django.views.generic import ListView
from core.models import Home

class Home(ListView):
    model = Home
    template_name = 'home.html'
