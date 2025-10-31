from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django_jalali.db import models as jmodels
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

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"