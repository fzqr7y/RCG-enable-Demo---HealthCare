from django.contrib import admin

# SC: see UserProfileInline below
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from demo.models import UserProfile

# Register your models here.

from .models import Post, Comment, Provider

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Provider)


# SC: extend User via UserProfile
# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user_profiles'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
