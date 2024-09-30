import decimal
from builtins import map, str
from django.contrib.auth.models import User
import os

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import (User, BaseUserManager, UserBalance,
                     UserTransaction, Profile, Deposit, WIthdrawals, MasterCard, System)


@receiver(post_save, sender=User)
def create_initial_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(
            user=instance,
            balance=0.00
        )


@receiver(post_save, sender=UserTransaction)
def save_transaction(sender, instance, created, **kwargs):
    if created:
        balance = UserBalance.objects.get(user=instance.user).balance
        if instance.transaction_type == "Deposit":
            user_balance = UserBalance.objects.get(
                user=instance.user
            )
            dep = Deposit.objects.get(user = instance.user)
            user_balance.balance += instance.amount
            user_balance.save()
            dep.balance += instance.amount
            dep.save()

        if instance.transaction_type == "Withdrawal" and balance >= instance.amount:
            user_balance = UserBalance.objects.get(
                user=instance.user,
            )
            withdrwal = WIthdrawals.objects.get(
                user=instance.user,
            )
            user_balance.balance -= instance.amount
            user_balance.save()
            withdrwal.balance += instance.amount
            withdrwal.save()

        if instance.transaction_type == "Transfer" and balance >= instance.amount:
            user_balance = UserBalance.objects.get(
                user=instance.user,
            )
            withdrwal = WIthdrawals.objects.get(
                user=instance.user,
            )
            user_balance.balance -= instance.amount
            user_balance.save()
            withdrwal.balance += instance.amount
            withdrwal.save()


        if instance.transaction_type == "Card Transaction" and balance >= instance.amount:
            user_balance = UserBalance.objects.get(
                user=instance.user,
            )
            withdrwal = WIthdrawals.objects.get(
                user=instance.user,
            )
            user_balance.balance -= instance.amount
            user_balance.save()
            withdrwal.balance += instance.amount
            withdrwal.save()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User)
def create_deposit(sender, instance, created, **kwargs):
    if created:
        Deposit.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_sytsem(sender, instance, created, **kwargs):
    if created:
        System.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_withdrawal(sender, instance, created, **kwargs):
    if created:
        WIthdrawals.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_card(sender, instance, created, **kwargs):
    if created:
        MasterCard.objects.create(user=instance)
