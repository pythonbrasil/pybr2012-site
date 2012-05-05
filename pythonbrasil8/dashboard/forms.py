from django.forms import ModelForm

from pythonbrasil8.dashboard.models import AccoutProfile


class AddUserForm(ModelForm):
    class Meta:
        model = AccoutProfile
