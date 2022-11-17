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

from Common.libs.choices import gender_choices, identification_card_type_choices, education_choices
from Common.utils.text_handler.random import random_content
from .base import BaseManager, Base, handle_object_does_not_exist
from .regions import Country, Province, City, Area, Street


class Language(Base):
    name = models.CharField(max_length=20, unique=True, verbose_name='语言名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='语言代码')

    class Meta:
        verbose_name = verbose_name_plural = '语言'

    def __str__(self):
        return self.name


class Race(Base):
    name = models.CharField(max_length=20, unique=True, verbose_name='人种名称')

    class Meta:
        verbose_name = verbose_name_plural = '人种'

    def __str__(self):
        return self.name


class Ethnicity(Base):
    name = models.CharField(max_length=20, unique=True, verbose_name='种族名称')

    class Meta:
        verbose_name = verbose_name_plural = '种族'

    def __str__(self):
        return self.name


class Nationality(Base):
    name = models.CharField(max_length=20, unique=True, verbose_name='民族名称')
    pinyin = models.CharField(max_length=32, unique=True, verbose_name='民族名称拼音')

    class Meta:
        verbose_name = verbose_name_plural = '民族'

    def __str__(self):
        return self.name


def random_username():
    return random_content(length=24, random_type='str_case')


def random_openid():
    return random_content(length=32, random_type='str_case')


def random_password():
    return random_content(length=16, random_type='password')


class UserManager(BaseManager, BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, password=None, **extra_fields):
        # if not username:
        #     raise ValueError('The given username must be set')
        username = username or random_username()
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password or random_password())
        user.openid = random_openid()
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_confirmed', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_admin_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_confirmed', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Admin user must have is_staff=True.')

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_confirmed', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_confirmed') is not True:
            raise ValueError('Superuser must have is_confirmed=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(Base, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, db_index=True, unique=True, verbose_name='用户名')
    nickname = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='昵称')
    openid = models.CharField(
        max_length=255, blank=True, null=True, default=None, db_index=True, verbose_name='给第三方用的openid')
    email = models.EmailField(max_length=32, blank=True, null=True, default=None, unique=True, verbose_name='邮箱')

    phone_number = models.CharField(max_length=32, blank=True, null=True, default=None, unique=True,
                                    verbose_name='手机号')
    name = models.CharField(max_length=64, blank=True, null=True, default=None, db_index=True, verbose_name='姓名')
    identification_card_type = models.IntegerField(
        choices=identification_card_type_choices, blank=True, null=True, default=1, verbose_name='证件类型')
    identification_card_number = models.CharField(
        max_length=32, blank=True, null=True, default=None, db_index=True, unique=True, verbose_name='身份证号')
    gender = models.IntegerField(choices=gender_choices, blank=True, null=True, default=0, verbose_name='性别')

    @property
    def sex(self):
        return self.gender

    @sex.setter
    def sex(self, sex):
        self.gender = sex

    age = models.SmallIntegerField(blank=True, null=True, default=None, verbose_name='年龄')
    birthday = models.DateField(blank=True, null=True, default=None, verbose_name='出生日期')
    native_place = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name='籍贯')
    nationality = models.ForeignKey(Nationality, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='民族')
    education = models.IntegerField(choices=education_choices, blank=True, null=True, default=-1,
                                    verbose_name='受教育程度')
    address = models.CharField(max_length=255, blank=True, null=True, default=None, verbose_name='地址')
    detailed_address = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name='详细住址')
    street = models.ForeignKey(Street, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='街道')
    area = models.ForeignKey(Area, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='区县')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='城市')
    province = models.ForeignKey(Province, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='省份')
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='国家')
    language = models.CharField(max_length=32, blank=True, null=True, default='zh_CN', verbose_name='使用语言')

    is_confirmed = models.BooleanField(blank=False, null=True, default=False, verbose_name='账户是否激活')
    # 用于查看区分用户是否长时间不使用
    is_active = models.BooleanField(blank=True, null=True, default=True, verbose_name='账户是否活跃')
    # 用于区分管理员用户
    is_staff = models.BooleanField(default=False, verbose_name='是否可以访问管理站点')

    # is_authenticated用于区分是否是匿名用户，不需要设置这个字段
    # is_superuser 指定该用户拥有所有权限，而不用一个个开启权限

    @property
    def is_admin(self):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        return False

    @property
    @handle_object_does_not_exist
    def is_manager(self):
        if self.is_admin:
            return True
        if self.is_active and self.is_authenticated and self.manager_role.is_active:
            return True
        return False

    @property
    @handle_object_does_not_exist
    def is_employee(self):
        if self.is_admin:
            return True
        if self.is_active and self.is_authenticated and self.employee_role.is_active:
            return True
        return False

    @property
    @handle_object_does_not_exist
    def is_student(self):
        if self.is_active and self.is_authenticated and self.student_role:
            return True
        return False

    @property
    @handle_object_does_not_exist
    def is_teacher(self):
        if self.is_active and self.is_authenticated and self.teacher_role:
            return True
        return False

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
