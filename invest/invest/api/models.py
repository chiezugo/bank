from builtins import ValueError, round, super, range
from PIL import Image
from datetime import datetime, timedelta
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone
import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
)


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def generate_activationcode(startwith='74', size=8, chars=string.digits):
    ref_id = startwith + ''.join(random.choice(chars) for x in range(size))
    try:
        id_exist = User.objects.get(user_ref_id=ref_id)
        if id_exist.exits():
            generate_activationcode(startwith='74', size=8, chars=string.digits)
    except:
        return startwith + ''.join(random.choice(chars) for x in range(size))

def generate_code(size=4, chars=string.digits):
    ref_id = ''.join(random.choice(chars) for x in range(size))
    try:
        id_exist = User.objects.get(user_ref_id=ref_id)
        if id_exist.exits():
            generate_activationcode(size=4, chars=string.digits)
    except:
        return ''.join(random.choice(chars) for x in range(size))

def generate_activationcod(startwith='08', size=7, chars=string.digits):
    ref_id = startwith + ''.join(random.choice(chars) for x in range(size))
    try:
        id_exist = User.objects.get(user_ref_id=ref_id)
        if id_exist.exits():
            generate_activationcod(startwith='08', size=7, chars=string.digits)
    except:
        return startwith + ''.join(random.choice(chars) for x in range(size))


def generate_mastercard(startwith='55', size=2, chars=string.digits):
    ref_id = startwith + ''.join(random.choice(chars) for x in range(size))
    try:
        id_exist = User.objects.get(user_ref_id=ref_id)
        if id_exist.exits():
            generate_mastercard(startwith='55', size=2, chars=string.digits)
    except:
        return startwith + ''.join(random.choice(chars) for x in range(size))


def generate_mastcard(size=4, chars=string.digits):
    ref_id = ''.join(random.choice(chars) for x in range(size))
    try:
        id_exist = User.objects.get(user_ref_id=ref_id)
        if id_exist.exits():
            generate_mastercard(size=4, chars=string.digits)
    except:
        return ''.join(random.choice(chars) for x in range(size))


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False,
                    is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not full_name:
            raise ValueError("Users must have surname and other names")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            user_ref_id=generate_activationcode(size=8)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, full_name, email, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,

            is_staff=True
        )
        return user

    def create_superuser(self, full_name, email, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,

            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_ref_id = models.CharField(max_length=255,default=generate_activationcode(),editable=False,
                                   unique=True)
    ac_num = models.CharField(max_length=255,default=generate_activationcode(),editable=False,
                                   unique=True)
    routing_num = models.CharField(max_length=255, default=generate_activationcod(size=7), editable=False,
                                   unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        unique_together = ('email', 'user_ref_id')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin





class UserTransaction(models.Model):
    class Meta:
        verbose_name = 'User Transactions'
        verbose_name_plural = 'User Transactuons'

    TRANSACTION_TYPE_CHOICES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Card Transaction', 'Card Transaction'),
        ('Transfer', 'Transfer'),
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(timezone.now())
    transaction_type = models.CharField(max_length=200, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.FloatField(default=0.00)
    trans_reference = models.CharField(max_length=255, default=create_ref_code, editable=False)
    bank = models.CharField(max_length=255, default='fells wargo')


    def __str__(self):
        return self.transaction_type

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(UserTransaction, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-id']

def len(balance):
    pass


def balance(args):
    pass

class MasterCard(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    code1 = models.CharField(max_length=255)
    code2 = models.CharField(max_length=255)
    code3 = models.CharField(max_length=255)
    cvv = models.CharField(max_length=255)
    requested = models.BooleanField(default=False)
    sum = models.CharField(max_length=55)
    date = models.DateTimeField(blank=True, null=True, )

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_mastercard(startwith='55', size=2, chars=string.digits)
            code1 = generate_mastcard(size=4, chars=string.digits)
            code2 = generate_mastcard(size=4, chars=string.digits)
            code3 = generate_mastcard(size=4, chars=string.digits)
            cvv = generate_mastcard(size=3, chars=string.digits)
            date = datetime.today()+ relativedelta(months=48)
            self.code = code
            self.code1 = code1
            self.code2 = code2
            self.code3 = code3
            self.cvv= cvv
            self.date = date
            self.sum = self.code + self.code1 + self.code2 + self.code3
        super().save(*args, **kwargs)

    def date_trunc_field(self):
        return self.date.date()

class RequestFund(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    requested = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.amount

    def get_fund_status(self):
        if self.accepted:
            user_balance_obj = UserBalance.objects.get(id=self.user.id).first()
            if user_balance_obj:
                user_balance_obj.balance += self.amount
                user_balance_obj.save()
                self.save()
        return self.amount


class Transfer(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    status = models.TextField(default='debit')
    receiver = models.CharField(max_length=255, )
    description = models.TextField(default='abc')
    trans_reference = models.CharField(max_length=255, default=create_ref_code, editable=False)
    amount = models.FloatField(default=0.00)
    transfer_date = models.DateTimeField(default=timezone.now(), null=False)
    bank = models.CharField(max_length=255, )

    def __str__(self):
        return self.trans_reference

    def save(self, *args, **kwargs):
        self.amount = round(self.amount, 2)
        super(Transfer, self).save(*args, **kwargs)


class UserBalance(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, related_name='user_balance')
    balance = models.FloatField(default=0.00)

    class Meta:
        verbose_name_plural = 'UserBalance'

    def save(self, *args, **kwargs):
        self.balance = round(self.balance, 2)
        super(UserBalance, self).save(*args, **kwargs)

class Bank(models.Model):
    bank = models.CharField(max_length=225)

    def __str__(self):
        return f"{self.bank}"

class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance = models.FloatField(default=0.00)

    def save(self, *args, **kwargs):
        self.balance = round(self.balance, 2)
        super(Deposit, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.user}"

class WIthdrawals(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    balance = models.FloatField(default=0.00)

    def save(self, *args, **kwargs):
        self.balance = round(self.balance, 2)
        super(WIthdrawals, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.user}"


class System(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    pin = models.CharField(max_length=20, default=generate_code())

    def __str__(self):
        return f'{self.user.email} Profile'

