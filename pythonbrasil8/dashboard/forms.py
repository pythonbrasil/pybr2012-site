# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea

from pythonbrasil8.dashboard.models import AccountProfile


class ProfileForm(ModelForm):

    class Meta:
        model = AccountProfile
        exclude = ('user', 'payement',)
        widgets = {
            'description': Textarea,
        }
