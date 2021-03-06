from django.contrib import admin

# SC: see UserProfileInline below
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Post, Comment
from .models import Provider, Member, Provider_Member, Member_Medical
from .models import County_Data, County_Widget, Member_Notification
from healthcare.models import UserProfile, Message

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Provider)
admin.site.register(Member)
admin.site.register(Provider_Member)
admin.site.register(Member_Medical)
admin.site.register(Member_Notification)
admin.site.register(Message)
admin.site.register(County_Data)
admin.site.register(County_Widget)


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
