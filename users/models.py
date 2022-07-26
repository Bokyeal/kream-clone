from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    SHOE_SIZE_CHOICES = [
        ("220", "220"),  # 앞에는 데이터베이스용, 뒤에는 우리가 보는 것
        ("230", "230"),
        ("235", "235"),
        ("240", "240"),
        ("245", "245"),
        ("250", "250"),
        ("255", "255"),
        ("260", "260"),
        ("265", "265"),
        ("270", "270"),
        ("275", "275"),
        ("280", "280"),
        ("285", "285"),
        ("290", "290"),
        ("295", "295"),
        ("300", "300"),
    ]

#verbose_name은 유저에게 보여지는거
    avatar = models.ImageField(verbose_name="아바타",
        blank=True, null=True
    )  # 이미지일 경우에만 null 사용, 나머지 charfield같은 애들은 null 사용안함
    phone_number = models.CharField(max_length=11)
    shoe_size = models.CharField(choices=SHOE_SIZE_CHOICES, max_length=3, blank=True)
    is_ad_message = models.BooleanField(default=False)
    is_ad_email = models.BooleanField(default=False)
