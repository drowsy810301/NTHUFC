from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from users.models import Account
from users.models import UserProfile


#Don't use built-in auth

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]



admin.site.unregister(User)
admin.site.unregister(Group)
#admin.site.register(User, UserAdmin)
admin.site.register(Account, UserAdmin)
