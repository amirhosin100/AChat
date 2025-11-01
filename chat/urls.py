from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("",views.index,name="index"),
    path("chat/my-groups/",views.my_groups,name="my_groups"),
    path("chat/group/<int:id>",views.group_detail,name="group_detail"),
    path("chat/group/<int:id>/settings",views.group_settings,name="group_settings"),
    path("chat/group/<int:id>/delete/",views.delete_group,name="delete_group"),
    path("chat/make-group/",views.make_group,name="make_group"),
    path("chat/change-group-name/",views.change_group_name,name="change_group_name"),
    path("chat/change-group-code/",views.change_group_code,name="change_group_code"),
]