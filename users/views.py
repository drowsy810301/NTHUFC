#coding=utf-8

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from users.forms import LoginForm
from django.core.urlresolvers import reverse
from photos.models import Photo,Tag
from users.models import Account
from index.forms import AccountCreationFrom, PhotoCreationForm
from django.forms.models import inlineformset_factory
from locationMarker.models import Marker
from photos.socialApplication import uploadPhoto, deletePhoto
from axes.utils import reset
from axes.decorators import watch_login, get_ip, FAILURE_LIMIT, get_user_attempts
from axes.models import AccessAttempt
# Create your views here.


def get_attemps(request):
    remain_times = 0
    att = 0
    try:
        attempts = AccessAttempt.objects.filter(ip_address=get_ip(request))
        if len(attempts) > 0:
            for attempt in attempts:
                att =  att + attempt.failures_since_start
        else:
            remain_times = FAILURE_LIMIT

    except:
        print 'something goes wrong!'

    remain_times = FAILURE_LIMIT - att
    return remain_times

@login_required
def users(request):
    account = request.user

    photos = account.photos.order_by('-votes')
    #sorted(photos,key=lambda x : x['favorites']+x['likes'],reverse=True)
    #print photos.count()

    form_number = 5 - photos.count();
    PhotoInlineFormSet = inlineformset_factory(Account, Photo,
    form=PhotoCreationForm, max_num=5, validate_max=True,
        min_num=1, validate_min=True, extra=form_number, can_delete=True)

    all_tags = Tag.objects.all()
    hot_tags = Tag.objects.order_by('-tag_count')[:5]
    recent_tags = Tag.objects.order_by('-update_time')[:5]
    if request.method == "POST":
        #form = AccountCreationFrom(request.POST, request.FILES, instance=account, prefix="main")
        formset = PhotoInlineFormSet(request.POST, request.FILES, instance=account, prefix="nested")
        #if form.is_valid() and formset.is_valid():

        if formset.is_valid():
            photoList = formset.save(commit=False)
            for photo in photoList:
                photo.rank = len(photo.content) + len(photo.tags.split(' '))*5;
                photo.save()
                uploadPhoto(photo)
            account.updatePhotosRank()
            return redirect(reverse('users:profile'))
        else:
            formset = PhotoInlineFormSet(instance=account, prefix="nested")
            return render(request, "users/profile.html", {
                "photos": photos,
                "formset": formset,
                "marker_list": Marker.objects.all(),
                "all_tags":[ x.tag_name for x in all_tags],
                "hot_tags":[ x.tag_name for x in hot_tags],
                "recent_tags":[ x.tag_name for x in recent_tags],
            })
    else:
        #form = AccountCreationFrom(instance=account, prefix="main")
        formset = PhotoInlineFormSet(instance=account, prefix="nested")
        return render(request, "users/profile.html", {
            "photos": photos,
            "formset": formset,
            "marker_list": Marker.objects.all(),
            "all_tags":[ x.tag_name for x in all_tags],
            "hot_tags":[ x.tag_name for x in hot_tags],
            "recent_tags":[ x.tag_name for x in recent_tags],
        })

@watch_login
def login(request):

    remain_times = 0
    remain_times = get_attemps(request)
    F = LoginForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                ID_card=form.cleaned_data['ID_card'])
            if user:
                auth_login(request, user)
                return redirect(reverse('users:profile'))

        else:
            remain_times = remain_times - 1
            return render(request, 'index/login.html', {'form': form, 'remain_times': remain_times })

    return render(request, 'index/login.html', {'form': form, 'remain_times': remain_times })


def logout(request):
    auth_logout(request)
    return redirect(reverse('index:index'))

@login_required()
def delete_photo(request, delete_id):

    photo_info = {}
    if delete_id != '':
        try:
            photo = Photo.objects.get(id=long(delete_id))
            user = photo.owner
            photo_info['facebook_post_id'] = photo.facebook_post_id
            photo_info['title'] = photo.title
            photo_info['location_marker_title'] = photo.location_marker.title
            photo_info['content'] = photo.content
            photo_info['flickr_photo_id'] = photo.flickr_photo_id
            photo_info['tags'] = photo.tags
            photo.delete()
            deletePhoto(photo_info)

            user.updatePhotosRank()
            print('Photo id %ld deletes successfully!' % long(delete_id))
        except Photo.DoesNotExist:
            print('Photo id %ld does not exist!' % long(delete_id))

    return redirect(reverse('users:profile'))


def locked_out(request):
    """Block login for over 3 wrong tries."""

    '''
    attempts = AccessAttempt.objects.filter(ip_address=get_ip(request))
    for attempt in attempts:
        if attempt.failures_since_start >= FAILURE_LIMIT:
            unblock_time = attempt.attempt_time + COOLOFF_TIME
    '''
    return render(request, 'users/lock_out.html', {})
    # No block attempt
    #return redirect(reverse('index:index'))

