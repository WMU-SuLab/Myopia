# -*- encoding: utf-8 -*-
"""
@File Name      :   user.py    
@Create Time    :   2022/4/4 15:51
@Description    :   
@Version        :   
@License        :   MIT
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from .base import Base


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_authenticated', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_authenticated', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_authenticated') is not True:
            raise ValueError('Superuser must have is_authenticated=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(Base, AbstractBaseUser, PermissionsMixin):
    gender_choices = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )
    identification_card_type_choices = (
        (0, '其他'),
        (1, '居民身份证'),
        (2, '港澳居民来往内地通行证'),
        (3, '台湾居民来往大陆通行证'),
        (4, '护照'),
        (5, '军官证'),
        (6, '士兵证'),
        (7, '外国人居留证'),
    )

    username = models.CharField(max_length=128, db_index=True, unique=True, verbose_name='用户名')
    nickname = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='昵称')
    openid = models.CharField(
        max_length=255, blank=True, null=True, default=None, db_index=True, verbose_name='给第三方用的openid')
    email = models.EmailField(max_length=32, blank=True, null=True, default=None, unique=True, verbose_name='邮箱')

    phone = models.CharField(max_length=32, blank=True, null=True, default=None, unique=True, verbose_name='手机号')
    name = models.CharField(max_length=64, blank=True, null=True, default=None, db_index=True, verbose_name='姓名')
    identification_card_type = models.IntegerField(
        max_length=1, choices=identification_card_type_choices,
        blank=True, null=True, default=1, verbose_name='证件类型')
    identification_card_number = models.CharField(
        max_length=32, null=True,
        blank=True, default=None, db_index=True, unique=True, verbose_name='身份证号')
    gender = models.CharField(
        max_length=32, choices=gender_choices, blank=True, null=True, default=0, verbose_name='性别')

    @property
    def sex(self):
        return self.gender

    @sex.setter
    def sex(self, sex):
        self.gender = sex

    age = models.SmallIntegerField(blank=True, null=True, default=None, verbose_name='年龄')
    birthday = models.DateField(blank=True, null=True, auto_now_add=True, verbose_name='出生日期')
    native_place = models.CharField(max_length=32, blank=True, null=True, default=None, verbose_name='籍贯')
    home_address = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='家庭住址')
    language = models.CharField(max_length=32, blank=True, null=True, default='zh_CN', verbose_name='使用语言')
    street = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='街道')
    city = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='城市')
    province = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='省份')
    country = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='国家')

    is_authenticated = models.BooleanField(blank=False, null=True, default=True, verbose_name='是否验证')
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name='是否活跃')
    is_staff = models.BooleanField(default=False, verbose_name='是否可以访问管理站点')

    # 用户管理器
    objects = UserManager()

    # 设置认证标识
    USERNAME_FIELD = 'username'
    # 当通过createsuperuser管理命令创建一个用户时，用于提示的一个字段名称列表
    # 不应该包含USERNAME_FIELD设置的字段和password字段
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        app_label = 'Common'
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return f'<User : {self.username}>'
