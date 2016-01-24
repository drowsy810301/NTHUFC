# -*- coding: utf-8 -*-
import re
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field, Div
from crispy_forms.bootstrap import  FormActions, InlineRadios
from users.models import Account
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from  django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    #username = forms.CharField()
    email = forms.EmailField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput,max_length=10)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # important!!!!! self.helper.form_tag = False
        self.helper.form_tag = False

        self.fields['email'].label = u'信箱'
        self.fields['password'].label = u'密碼'
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    u'登入',
                    Field('email'),
                    Field('password'),
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
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = Account.objects.get(email=email)
            if not check_password(password, user.password):
                raise forms.ValidationError("登入失敗")
        except Account.DoesNotExist:
            raise forms.ValidationError("登入失敗")

        return cleaned_data

class ForgetPasswordForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # important!!!!! self.helper.form_tag = False
        self.helper.form_tag = False
        self.fields['username'].label = u'姓名'
        self.fields['email'].label = u'信箱'
    
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    u'忘記密碼',
                    Field('username'),
                    Field('email'),
                    HTML('<br>')
                ),
                FormActions(
                    Submit('submit', u'提交', css_class='btn btn-primary'),
                    css_class="submit-btn"
                ),
                css_class="forget-password-form",
            ),
        )        
        
    def clean(self):
        cleaned_data = self.cleaned_data
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")

        try:
            user = Account.objects.get(username=username, email=email)            
        except Account.DoesNotExist:
            raise forms.ValidationError("提交失敗")

        return cleaned_data
        
class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput,max_length=10)
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=10)
    
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # important!!!!! self.helper.form_tag = False
        self.helper.form_tag = False
        self.fields['password'].label = u'新密碼'
        self.fields['confirm_password'].label = u'確認密碼'
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': u'請輸入新密碼, 須由6~10個英文或數字組成'})
        
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    u'重設密碼',
                    Field('password'),
                    Field('confirm_password'),
                    HTML('<br>')
                ),
                FormActions(
                    Submit('submit', u'提交', css_class='btn btn-primary'),
                    css_class="submit-btn"
                ),
                css_class="reset-password-form",
            ),
        )    
    
    def clean_password(self):
        password = self.cleaned_data.get("password")        

        if not re.match(r'^[A-Za-z0-9]{6,10}$',password):
            raise forms.ValidationError(u'密碼必須由6~10個英文或數字組成',code='wrong_password_format')
        return password
    '''
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        print password
        print confirm_password
        if password != confirm_password:
            raise forms.ValidationError(u'兩次輸入的密碼不一致',code='password_mismatch')

        return confirm_password
    '''    
    
    def clean(self):        
        cleaned_data = self.cleaned_data
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")       
        
        if(password!= None and password != confirm_password):
            raise forms.ValidationError("密碼不一致")

        return cleaned_data
        