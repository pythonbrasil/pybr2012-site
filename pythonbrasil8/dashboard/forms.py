from django.forms import ModelForm

from pythonbrasil8.dashboard.models import AccountProfile


class ProfileForm(ModelForm):

    class Meta:
        model = AccountProfile
