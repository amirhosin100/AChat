from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User
class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("phone","first_name","last_name")

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("phone","first_name","last_name","is_staff",
                  "is_superuser","is_active","date_of_birth","bio",
                  "date_joined","last_login")


