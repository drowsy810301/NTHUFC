# -*- coding: utf-8 -*-
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field, Div
from crispy_forms.bootstrap import  FormActions, InlineRadios
from users.models import Account
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    ID_card = forms.CharField(max_length=10, validators=[RegexValidator(regex='^([A-Z][12]\d{8})$', message='Invalid ID', code='Invalid ID')])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # important!!!!! self.helper.form_tag = False
        self.helper.form_tag = False

        self.fields['username'].label = u'姓名'
        self.fields['email'].label = u'信箱'
        self.fields['ID_card'].label = u'身份證'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    u'登入',
                    Field('username'),
                    Field('email'),
                    Field('ID_card'),
                    HTML('<br>')
                ),
                FormActions(
                    Submit('submit', u'登入', css_class='btn btn-primary'),
                    css_class="submit-btn"
                ),
                css_class="login-form",
            ),
        )




    def clean(self):
        cleaned_data = self.cleaned_data
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        ID_card = self.cleaned_data.get("ID_card")

        try:
            user = Account.objects.get(username=username, email=email, ID_card=ID_card)
        except Account.DoesNotExist:
            raise forms.ValidationError("登入失敗")

        return cleaned_data

