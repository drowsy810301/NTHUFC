# -*- coding: utf-8 -*-
from django import forms
from users.models import Account
from photos.models import Photo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field, Div
from crispy_forms.bootstrap import  FormActions, InlineRadios, PrependedText
from django.contrib.auth.models import User
import re

class AccountCreationFrom(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput,max_length=10)
    class Meta:
        model = Account
        fields = ('username', 'nickname', 'password', 'identity', 'major', 'email', 'cellphone', 'is_agree')

    def __init__(self, *args, **kwargs):
        super(AccountCreationFrom, self).__init__(*args, **kwargs)
        # Set layout for fields.
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'

        link = '<a data-toggle="modal" data-target="#rule" style="cursor:pointer">' + \
                 u'同意參賽規則' + '</a>'
        self.fields['username'].label = u'姓名'
        self.fields['nickname'].label = u'暱稱'
        self.fields['password'].label = u'密碼'
        self.fields['confirm_password'].label = u'確認密碼'
        self.fields['identity'].label = u'身份'
        self.fields['major'].label = u'系所或單位'
        self.fields['email'].label = u'電子郵件'
        self.fields['cellphone'].label = u'手機'
        self.fields['is_agree'].label = link

        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': u'請填寫真實姓名,將來領獎的時候會用來驗證您的身分'})
        self.fields['nickname'].widget = forms.TextInput(attrs={'placeholder': u'建議取特別的暱稱，以便與其他參賽者區隔'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': u'密碼必須由6~10個英文或數字組成,忘記請與我們聯繫','maxlength':10})
        self.fields['email'].widget = forms.PasswordInput(attrs={'placeholder': u'email會作為您的帳號喔'})

        self.helper.layout = Layout(
            Fieldset(
                u'報名資料',
                Field('username'),
                Field('nickname'),
                Field('password'),
                Field('confirm_password'),
                Field('email'),
                Field('cellphone'),
                InlineRadios('identity'),
                Field('major'),
                Div(
                    Field('is_agree'),
                    css_class='col-lg-offset-9 col-lg-4',
                ),
            ),
            Div(
                HTML('<hr>'),
                css_class='account-hr'
            ),
            #type="Submit" name="submit" value="確定送出" class="btn btn-primary"
            #FormActions(
                #Submit('submit', u'確定送出', css_class='btn btn-primary'),
                #css_class="submit-btn"
            #)
        )

    def clean_is_agree(self):
        cleaned_data = self.cleaned_data
        is_agree = self.cleaned_data.get("is_agree")

        if not is_agree:
            raise forms.ValidationError(u'尚未同意參賽規則',code='not_agree')

        return is_agree

    def clean_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if not re.match(r'^[A-Za-z0-9]{6,10}$',password):
            raise forms.ValidationError(u'密碼必須由6~10個英文或數字組成',code='wrong_password_format')

        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(u'兩次輸入的密碼不一致',code='password_mismatch')

        return confirm_password


class PhotoCreationForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'content','tags','location_marker','image')

    def __init__(self, *args, **kwargs):
        super(PhotoCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # important!!!!! self.helper.form_tag = False
        self.helper.form_tag = False
        self.fields['content'].widget.attrs['rows'] = 4
        self.fields['content'].widget.attrs['columns'] = 15
        self.fields['image'].widget.attrs['accept'] = "image/*"

        self.helper.layout = Layout(
            Div(
                Fieldset(
                    u'選擇相片',
                    Field('title'),
                    Field('content'),
                    Field('tags'),
                    Field('location_marker'),
                    Field('image'),
                    HTML('<br>')
                ),
                css_class="image-form"
            ),
        )
