
# coding: utf-8
from __future__ import unicode_literals

from authentication.models import Account

__author__ = 'jujbob'

from django import forms

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password', )