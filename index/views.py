#-*- encoding=UTF-8 -*-
from django.shortcuts import render, redirect
from photos.models import Photo,Tag
from users.models import Account
from index.forms import AccountCreationFrom, PhotoCreationForm
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from locationMarker.models import Marker
from photos.socialApplication import uploadPhoto

# Create your views here.
def index(request):
    #test related_name
    '''
    test_account = Account.objects.all()[:1].get()
    all_photos = test_account.photos.all()
    '''
    return render(request, "index/index.html", {})

def participate(request, id_account=None):
    if id_account is None:
        account = Account()
        PhotoInlineFormSet = inlineformset_factory(Account, Photo,
            form=PhotoCreationForm, max_num=5, validate_max=True,
            min_num=1, validate_min=True, extra=5, can_delete=False)
    else:
        account = Account.objects.get(pk=id_account)
        PhotoInlineFormSet = inlineformset_factory(Account, Photo,
            form=PhotoCreationForm, max_num=5, validate_max=True,
            min_num=1, validate_min=True, extra=5, can_delete=True)


    if request.method == "POST":
        form = AccountCreationFrom(request.POST, request.FILES, instance=account, prefix="main")
        formset = PhotoInlineFormSet(request.POST, request.FILES, instance=account, prefix="nested")

        if form.is_valid() and formset.is_valid():
            form.save()
            photoList = formset.save(commit=False)
            for photo in photoList:
                photo.save()
                uploadPhoto(photo)
            return redirect(reverse('index:index'))
    else:

        form = AccountCreationFrom(instance=account, prefix="main")
        formset = PhotoInlineFormSet(instance=account, prefix="nested")
        all_tags = Tag.objects.all()
        hot_tags = Tag.objects.order_by('-tag_count')[:5]
        recent_tags = Tag.objects.order_by('-update_time')[:5]
        return render(request, "index/participate.html", {
            "form":form,
            "formset": formset,
            "marker_list": Marker.objects.all(),
            "all_tags":[ x.tag_name for x in all_tags],
            "hot_tags":[ x.tag_name for x in hot_tags],
            "recent_tags":[ x.tag_name for x in recent_tags],
        })
