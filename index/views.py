#-*- encoding=UTF-8 -*-
from django.shortcuts import render, redirect
from photos.models import Photo,Tag
from users.models import Account
from index.forms import AccountCreationFrom, PhotoCreationForm
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from locationMarker.models import Marker
from photos.socialApplication import uploadPhoto
from django.contrib import messages
from photos.models import Photo
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

# Create your views here.
def index(request):
    top_five = Photo.objects.all().order_by('-votes')[:5]
    return render(request, "index/index.html", {'photos': top_five})

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

    all_tags = Tag.objects.all()
    hot_tags = Tag.objects.order_by('-tag_count')[:5]
    recent_tags = Tag.objects.order_by('-update_time')[:5]
    if request.method == "POST":
        form = AccountCreationFrom(request.POST, request.FILES, instance=account, prefix="main")
        formset = PhotoInlineFormSet(request.POST, request.FILES, instance=account, prefix="nested")


        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            ID_card = form.cleaned_data['ID_card']

            if formset.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Photos are uploading...')
                form.save()
                photoList = formset.save(commit=False)
                for photo in photoList:
                    photo.rank = len(photo.content) + len(photo.tags.split(' '))*5;
                    photo.save()
                    uploadPhoto(photo)

                user = authenticate(username=username, email=email, ID_card=ID_card)
                user.updatePhotosRank()
                if user:
                    auth_login(request, user)
                else:
                    print 'login failed'

                return redirect(reverse('index:index'))
            else:
                messages.add_message(request, messages.ERROR, 'At least upload one photo!')

        return render(request, "index/participate.html",{
            "form":form,
            "formset": formset,
            "marker_list": Marker.objects.all(),
            "all_tags":[ x.tag_name for x in all_tags],
            "hot_tags":[ x.tag_name for x in hot_tags],
            "recent_tags":[ x.tag_name for x in recent_tags],
        })
    else:

        form = AccountCreationFrom(instance=account, prefix="main")
        formset = PhotoInlineFormSet(instance=account, prefix="nested")
        return render(request, "index/participate.html", {
            "form":form,
            "formset": formset,
            "marker_list": Marker.objects.all(),
            "all_tags":[ x.tag_name for x in all_tags],
            "hot_tags":[ x.tag_name for x in hot_tags],
            "recent_tags":[ x.tag_name for x in recent_tags],
        })

def q_a(request):
    return render(request, 'index/q_a.html')

def map(request):
    if request.method =="GET":
        query = request.GET.get('search', False)
        q = request.GET.get('search')
        photos = Photo.objects.filter(tags__contains=query) | Photo.objects.filter(title__contains=query) | Photo.objects.filter(content__contains=query)
        markers = []
        tmp = []
        for photo in photos:
            markers.append(photo.location_marker)
            tmp2 = photo.tags.split()
            for tag in tmp2:
                tmp.append(tag)
        tags = list(set(tmp))

    return render(request, "index/map.html",
        {
            'photos': photos,
            'query': q,
            'marker_list':markers,
            'tags': tags,
        })
