from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django_jalali.db import models as jmodels
from django.urls import reverse

import random
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,phone,first_name,password=None):

        if not phone:
            raise ValueError("users must have a phone number")

        user = self.model(phone=phone,first_name=first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone,first_name,password=None):

        user = self.create_user(phone, first_name,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=11,unique=True,verbose_name="شماره تلفن")

    first_name = models.CharField(max_length=50,verbose_name="نام")
    last_name = models.CharField(max_length=50,blank=True,verbose_name="نام خانوادگی")

    date_of_birth = jmodels.jDateField(blank=True,null=True,verbose_name="تاریخ تولد")
    bio = models.TextField(max_length=500,blank=True,null=True,verbose_name="بیوگرافی")

    date_joined = jmodels.jDateTimeField(default=timezone.now,verbose_name="تاریخ ثبت نام")

    last_login = jmodels.jDateTimeField("آخرین ورود",blank=True, null=True)

    is_active = models.BooleanField(default=True,verbose_name="فعال بودن")
    is_staff = models.BooleanField(default=False,verbose_name="کارمند بودن")
    objects = UserManager()

    REQUIRED_FIELDS = ["first_name"]

    USERNAME_FIELD = "phone"

    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.first_name and self.last_name :
            return f"{self.first_name} {self.last_name}"
        elif self.first_name :
            return self.first_name
        elif self.last_name :
            return self.last_name
        return  ""

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

def set_unique(length=15):
    characters = "abcdefghijklmnopqrstuvwxyz"
    code = random.choices(characters,k=length)
    if ChatGroup.objects.filter(unique_code=code).exists() :
        set_unique(length)
    return "".join(code)

class ChatGroup(models.Model):
    creator = models.ForeignKey(User,models.CASCADE,"my_groups")
    name = models.CharField("نام",max_length=50)
    unique_code = models.CharField(max_length=15,default=set_unique,unique=True)
    create = jmodels.jDateTimeField(verbose_name="تاریخ ایجاد",auto_now=True)

    class Meta :
        ordering = [
            "-create"
        ]
        indexes = [
            models.Index(fields=["-create"])
        ]
        verbose_name = "گروه"
        verbose_name_plural = "گروه ها"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chat:group_detail",args=[self.id])

class Member(models.Model):
    user = models.ForeignKey(User,models.CASCADE,verbose_name="کاربر",related_name="joined_groups")
    chat = models.ForeignKey(ChatGroup,models.CASCADE,related_name="members",verbose_name="گروه")
    date_joined = jmodels.jDateTimeField("تاریخ ورود",auto_now=True)


class Message(models.Model):
    user = models.ForeignKey(User,models.CASCADE,verbose_name="کاربر")
    chat = models.ForeignKey(ChatGroup,models.CASCADE,"messages","گروه")
    text = models.TextField(max_length=1000,verbose_name="متن")
    create = jmodels.jDateTimeField("تاریخ ارسال",auto_now_add=True)

    class Meta :
        ordering = [
            "create"
        ]
        indexes = [
            models.Index(fields=["create"])
        ]