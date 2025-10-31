from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from chat.forms import *
from chat.models import *
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_filter =  ("is_active","is_staff","is_superuser")
    list_display = ("phone","first_name","last_name","date_of_birth")
    ordering = ("phone",)

    fieldsets = [
        (None,{"fields":("phone","password")}),
        ("اطلاعات شخصی",{"fields":("first_name","last_name","date_of_birth","bio")}),
        ("مجوز ها",{"fields":("is_superuser","is_staff","is_active","groups","user_permissions")}),
        ("تاریخ ها",{"fields":("last_login","date_joined")}),

    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "first_name", "password1", "password2"],
            },
        ),
    ]

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    list_display = ("name","creator","create")
    raw_id_fields = ("creator",)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("user","chat","date_joined")
    raw_id_fields = ("chat", "user")

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("user","chat","text","create")
    raw_id_fields = ("chat","user")