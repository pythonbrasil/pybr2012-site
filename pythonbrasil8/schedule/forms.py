from django.forms import ModelForm

from pythonbrasil8.schedule.models import Session


class SessionForm(ModelForm):

    class Meta:
        model = Session
