from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import User
from django import forms

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

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.widgets.PasswordInput())
    class Meta :
        model = User
        fields = ["phone","first_name","last_name","password","password2"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if User.objects.filter(phone=phone).exists() :
            raise forms.ValidationError("شماره از قبل وجود دارد")
        elif not phone.isdigit() :
            raise forms.ValidationError("شماره تلفن عددی است")
        elif not phone.startswith("09") :
            raise forms.ValidationError("شماره تلفن باید از 09 شروع شود")

        return phone

    def clean_password2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if password2 != password :
            raise forms.ValidationError("پسورد ها با هم مطابقت ندارند")

        return password2
