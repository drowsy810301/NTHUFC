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
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
@ensure_csrf_cookie
def index(request):
    top_five = Photo.objects.filter(isReady=True).order_by('-votes')[:5]
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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if formset.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Photos are uploading...')
                form.save()
                photoList = formset.save(commit=False)
                for photo in photoList:
                    photo.rank = len(photo.content) + len(photo.tags.split(' '))*5;
                    photo.save()
                    #uploadPhoto(photo)

                user = authenticate(email=email, password = password)
                user.updatePhotosRank()
                if user:
                    auth_login(request, user)
                else:
                    print 'login failed'

                return redirect(reverse('users:profile'))
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
def poster(request):
    return render(request, 'index/poster.html')
def privacypolicy(request):
    return render(request, 'index/privacypolicy.html')

def map(request):
    if request.method =="GET":
        query = request.GET.get('search', '')
        photos = Photo.objects.filter(isReady=True, tags__contains=query) | Photo.objects.filter(isReady=True, title__contains=query) | Photo.objects.filter(isReady=True, content__contains=query)
        photos = photos.order_by('rank').reverse()
        markers = []
        tagdic = dict()
        markerdic = dict()
        for photo in photos:
            photo.content = photo.content.replace("\r\n","")
            markers.append(photo.location_marker)
            if photo.location_marker.title in markerdic:
                markerdic[photo.location_marker.title] = markerdic[photo.location_marker.title] + 1
            else:
                markerdic[photo.location_marker.title] = 1

            tmp2 = photo.tags.split()
            for tag in tmp2:
                if tag in tagdic:
                    tagdic[tag] = tagdic[tag] + 1
                else:
                    tagdic[tag] = 1;

    return render(request, "index/map.html",
        {
            'photos': photos,
            'query': query,
            'marker_list':markers,
            'tagdic': tagdic,
            'markerdic': markerdic,
        })

