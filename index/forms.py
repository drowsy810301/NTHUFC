# -*- coding: utf-8 -*-
from django import forms
from users.models import Account
from photos.models import Photo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML, Field, Div
from crispy_forms.bootstrap import  FormActions, InlineRadios
from django.contrib.auth.models import User

class AccountCreationFrom(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', 'nickname', 'identity', 'major', 'email', 'cellphone')

    def __init__(self, *args, **kwargs):
        super(AccountCreationFrom, self).__init__(*args, **kwargs)
        # Set layout for fields.
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['username'].label = u'姓名'
        self.fields['nickname'].label = u'暱稱'
        self.fields['identity'].label = u'身份'
        self.fields['major'].label = u'系所或單位'
        self.fields['email'].label = u'信箱'
        self.fields['cellphone'].label = u'手機'

        self.helper.layout = Layout(
            Fieldset(
                u'報名資料',
                Field('username'),
                Field('nickname'),
                Field('email'),
                Field('cellphone'),
                InlineRadios('identity'),
                Field('major')
            ),
            #type="Submit" name="submit" value="確定送出" class="btn btn-primary"
            #FormActions(
                #Submit('submit', u'確定送出', css_class='btn btn-primary'),
                #css_class="submit-btn"
            #)
        )

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
                    u'上傳相片',
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
