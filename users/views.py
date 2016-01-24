#-*- encoding=UTF-8 -*-
import hashlib
import random
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import ensure_csrf_cookie
from users.forms import LoginForm, ForgetPasswordForm, ResetPasswordForm
from django.core.urlresolvers import reverse
from photos.models import Photo,Tag
from users.models import Account, UserProfile
from index.forms import AccountCreationFrom, PhotoCreationForm
from django.forms.models import inlineformset_factory
from locationMarker.models import Marker
from photos.socialApplication import uploadPhoto, deletePhoto
from axes.utils import reset
from axes.decorators import watch_login, get_ip, FAILURE_LIMIT, get_user_attempts
from axes.models import AccessAttempt
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from threading import Thread

from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
user_logged_in.disconnect(update_last_login)
# Create your views here.



def send_forget_password_email(request, user):
    username = user.username
    email = user.email
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+email).hexdigest()
    
    #Create and save user profile
    UserProfile.objects.filter(account=user).delete()
    new_profile = UserProfile(account=user, activation_key=activation_key)
    new_profile.save()

    # Send email with activation key
    profile_link = request.META['HTTP_HOST'] + \
        reverse('users:forget_password_confirm', kwargs={'activation_key': activation_key})
    email_subject = 'Password Reset'
    email_body = render_to_string('index/forget_password_email.html',
                    {'username': username, 'profile_link': profile_link,
                    'active_time': new_profile.active_time})
    msg = EmailMultiAlternatives(email_subject, email_body, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(email_body, "text/html")

    try:
        Thread(target=msg.send, args=()).start()
    except:
        print ("There is an error when sending email to %s's mailbox" % username)

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
@ensure_csrf_cookie
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
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            if user:
                auth_login(request, user)
                return redirect(reverse('users:profile'))
            else:
                remain_times = remain_times - 1
                return render(request, 'index/login.html', {'form': form, 'remain_times': remain_times})
        else:
            remain_times = remain_times - 1
            return render(request, 'index/login.html', {'form': form, 'remain_times': remain_times })

    return render(request, 'index/login.html', {'form': form, 'remain_times': remain_times })

def forget_password(request):
    if request.user.is_authenticated():
        return redirect(reverse('index:index'))
    
    F = ForgetPasswordForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(data=request.POST)
        if form.is_valid():
            user = Account.objects.get(username=form.cleaned_data['username'], email=form.cleaned_data['email'])           
            if user:
                send_forget_password_email(request, user)
                messages.add_message(request, messages.SUCCESS, '信件已寄送')
            else:               
                return render(request, 'index/forget_password.html', {'form': form})

        else:            
            return render(request, 'index/forget_password.html', {'form': form})

    return render(request, 'index/forget_password.html', {'form': form})

def forget_password_confirm(request, activation_key):
    """check if user is already logged in and if he
    is redirect him to some other url, e.g. home
    """
    if request.user.is_authenticated():
        return redirect(reverse('index:index'))

    '''check if there is UserProfile which matches
    the activation key (if not then display 404)
    '''
    # clear expired activation_key
    UserProfile.objects.filter(active_time__lte=datetime.datetime.now()).delete()

    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    user = user_profile.account

    user.backend = 'users.backends.EmailAuthBackend'
    #user.is_active = True
    user.save()
    # Let user login, so as to modify password
    auth_login(request, user)
    print ('User %s is ready to reset his/her password' % user.username)
    return redirect(reverse('users:reset_password'))

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

def reset_password(request):   
    
    F = ResetPasswordForm
    if request.method == 'GET':
        form = F()
    else:
        form = F(data=request.POST)
        if form.is_valid():
            try:
                request.user.reset_password(form.cleaned_data['password'])                 
                messages.add_message(request, messages.SUCCESS, '更改成功')
                return redirect(reverse('index:index'))
            except:
                print 'reset failed'
                return render(request, 'index/reset_password.html', {'form': form})          

        else:            
            return render(request, 'index/reset_password.html', {'form': form})

    return render(request, 'index/reset_password.html', {'form': form})
    
def locked_out(request):
    """Block login for over 5 wrong tries."""

    '''
    attempts = AccessAttempt.objects.filter(ip_address=get_ip(request))
    for attempt in attempts:
        if attempt.failures_since_start >= FAILURE_LIMIT:
            unblock_time = attempt.attempt_time + COOLOFF_TIME
    '''
    return render(request, 'users/lock_out.html', {})
    # No block attempt
    #return redirect(reverse('index:index'))

