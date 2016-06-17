
# coding: utf-8
from __future__ import unicode_literals

from authentication.models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

__author__ = 'jujbob'

from django import forms

class AccountForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', )

class AccountFormDetail(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'small_image', 'introduction', 'password1', 'password2', )


'''
    username = forms.RegexField(label="username", max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text="Required. 30 characters or fewer. Letters, digits and "
                                          "@/./+/-/_ only.",
                                error_messages={
                                    'invalid': "This value may contain only letters, numbers and "
                                               "@/./+/-/_ characters."},
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    #       'placeholder': 'Username',
                                    'required': 'true',
                                }))

    password1 = forms.CharField(label="password",
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    #       'placeholder': 'Password',
                                    'required': 'true',
                                }))

    password2 = forms.CharField(label="password confirmation",
                                help_text="Enter the same password as above, for verification.",
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    #       'placeholder': 'Password confirmation',
                                    'required': 'true',
                                })),

'''