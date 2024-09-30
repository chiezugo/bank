from builtins import float, Exception, super, str, type
from django.core.paginator import Paginator

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

import threading
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, Http404
from django.template.loader import render_to_string
from django.utils import timezone
from decimal import Decimal

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import is_safe_url
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.utils.http import is_safe_url
import random
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, FormView, View, DetailView, ListView
from .forms import LoginForm
from django.contrib import messages
from .forms import (RegisterForm, UserUpdateForm, ProductForm,
                    TransferForm, BanksForm, RequestForm, ProfileUpDateForm, PinForm)
from .models import (UserBalance, UserTransaction,
                     WIthdrawals, Deposit, Profile, User, Transfer, RequestFund, MasterCard, System)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if form.is_valid:
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                try:
                    del request.session['quest_email_id']
                except:
                    pass
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    current_site = get_current_site(request)
                    plaintext = get_template('email_templates/welcome.txt')
                    htmly = get_template('email_templates/welcom.html')
                    d = {'user': user,
                         'domain': current_site.domain,
                         }

                    subject, from_email, to = ' Fscbk Online Banking Alert', settings.EMAIL_HOST_USER, email,
                    text_content = plaintext.render(d)
                    html_content = htmly.render(d)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    return redirect('api:dashboard')
            messages.info(self.request, 'invalid email or password')
            return super(LoginView, self).form_invalid(form)
        return super(LoginView, self).form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('api:home')
    # Redirect to a success page.

def main_home_view(request):
    form = LoginForm()
    return render(request, 'home.html', {'form': form})

def insurance_view(request):
    return render(request, 'insurance.html')

def location_view(request):
    return render(request, 'locations.html')


def manage_view(request):
    return render(request, 'management.html')

def home_view(request):
    return render(request, 'homee.html')


@login_required
def user_dashboard_view(request):
    obj = UserBalance.objects.get(user=request.user)
    user_trans = UserTransaction.objects.filter(user=request.user).order_by('-id')[:2]
    withdrawal = WIthdrawals.objects.get(user=request.user)
    deposit = Deposit.objects.get(user=request.user)
    user_b = UserBalance.objects.get(user=request.user)
    form = TransferForm()
    context = {
        'withdrawal': withdrawal,
        'deposit': deposit,
        'obj': obj,
        'user_b': user_b,
        'form': form,
        'user_trans': user_trans
    }
    return render(request, 'dashboard.html', context)

@login_required
def create_card_view(request):
    new_card = MasterCard.objects.create(user=request.user)
    new_card.save()
    return redirect('api:card')

@login_required
def card_view(request):
    user = UserBalance.objects.get(user=request.user)
    master = MasterCard.objects.filter(user=request.user)
    item = UserTransaction.objects.filter(user=request.user, transaction_type = 'Card Transaction').order_by('-id')[:2]
    paginator = Paginator(item, 4)  # Show 4 contacts per page.
    page_number = request.GET.get('page')
    item = paginator.get_page(page_number)

    context = {
        'user': user,
        'master': master,
        'item': item,
        'page_obj': item,
    }
    return render(request, 'cards.html', context)

@login_required
def transactions_view(request):
    user = UserBalance.objects.get(user=request.user)
    item = UserTransaction.objects.filter(user=request.user)
    paginator = Paginator(item, 4)  # Show 4 contacts per page.
    page_number = request.GET.get('page')
    item = paginator.get_page(page_number)
    context = {
        'user': user,
        'item': item,
        'page_obj': item, }
    return render(request, 'transactions.html', context)


@login_required
def settings_view(request):
    user = UserBalance.objects.get(user=request.user)
    profile = Profile.objects.filter(user=request.user)
    context = {
        'user': user,
        'profile': profile, }
    return render(request, 'setting.html', context)



@login_required
def request_fund_view(request):
    form = RequestForm(request.POST or None)
    if form.is_valid():
        print(form)
        amount = form.cleaned_data.get('amount')
        amount = Decimal(amount.strip())
        description = form.cleaned_data.get('description')
        fund = RequestFund()
        fund.user = request.user
        fund.description = description
        fund.amount = amount
        fund.requested = True
        fund.save()
        return redirect("bank:request-fund")
    else:
        form = RequestForm()
    context = {
        'form': form,
    }
    return render(request, "accounts/fund.html", context)

@login_required
def change_pin_view(request):
    form = PinForm(request.POST or None)
    if form.is_valid():
        pin = form.cleaned_data.get("pin")
        newpin = form.cleaned_data.get("newpin")
        profile = Profile.objects.filter(user=request.user, pin=pin)
        if not profile:
            messages.warning(request, 'incurrect pin')
            return redirect('api:change-pin')
        profile.pin = newpin
        profile.update()
        messages.info(request, 'pin changed successfully')
        return redirect('api:change-pin')
    context = {
        'form': form
    }
    return render(request, 'pin_change.html', context)

@login_required
def transfer_view(request):
    form = TransferForm(request.POST or None)
    user = UserBalance.objects.get(user=request.user)
    if form.is_valid():
        amount = form.cleaned_data.get('amount')
        amount = float(amount.strip())
        description = form.cleaned_data.get('description')
        user_identity = form.cleaned_data.get('user_identity')
        bank = form.cleaned_data.get('bank')
        pin = form.cleaned_data.get('pin')
        profile = Profile.objects.filter(user=request.user, pin = pin)
        syst = System.objects.filter(user=request.user, active=True)
        if not syst:
            messages.info(request, 'You account is temporary blocked, please visit our nearest branch')
            return redirect("api:dashboard")
        if not profile:
            messages.info(request, 'Incorrect transfer code')
            return redirect("api:dashboard")
        try:
            receiver = User.objects.get(ac_num=user_identity, active=True)
            receiver_balance = UserBalance.objects.get(user=receiver)
            if user.balance > amount:
                user.balance -= amount
                user.save()
                receiver_balance.save()
                transfer = UserTransaction()
                transfer.user = request.user
                transfer.description = 'Transfer'
                transfer.bank = bank
                transfer.date = timezone.now()
                transfer.amount = amount
                transfer.save()
                user1 = UserBalance.objects.get(user=request.user)
                user_t = UserTransaction.objects.filter(user=request.user).order_by('-id').first()
                current_site = get_current_site(request)
                plaintext = get_template('email_templates/welcome.txt')
                htmly = get_template('email_templates/transaction_mail.html')
                d = {'description': description,
                     'user1': user1,
                     'user_identity': user_identity,
                     'amount': amount,
                     'user_t': user_t,
                     'domain': current_site.domain,
                         }

                subject, from_email, to = ' Fscbk Online Banking Alert', settings.EMAIL_HOST_USER, user.user.email,
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.info(request, 'Transfer successful')
                return redirect("api:dashboard")
            else:
                messages.info(request, 'Insufficient balance to perform transaction')
                return redirect("api:dashboard")
        except ObjectDoesNotExist:
            messages.info(request, 'please crosscheck the account number')
            return redirect("api:dashboard")

def admin_transfer_list_view(request):
    tf = Transfer.objects.all()
    context = {
        'tf': tf
    }
    return render(request, 'accounts/admin-transfer-list.html', context)


def transfer_update_view(request, id):
    obj = get_object_or_404(Transfer, id=id)
    form = ProductForm(instance=obj)
    if request.method == 'POST':
        form = ProductForm(request.POST or None, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            form = ProductForm()
    context = {
        'form': form,
        'obj': obj,
    }
    return render(request, 'accounts/assets_create.html', context)


@login_required
def transfer_delete_view(request, id):
    obj = get_object_or_404(Transfer, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('bank:user-transfer')
    context = {
        'object': obj
    }
    return render(request, "accounts/transfer-item.html", context)


@login_required
def transaction_delete_view(request, id):
    obj = get_object_or_404(UserTransaction, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('bank:transactions')
    context = {
        'object': obj
    }
    return render(request, "accounts/transactiondelete.html", context)


def profile_update_view(request):
    if request.method == 'POST':
        p_form = ProfileUpDateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if p_form.is_valid:
            p_form.save()
            print(p_form)
            messages.info(request, 'your profile is successfully updated')
            return redirect('bank:user-dashboard')
    else:
        p_form = ProfileUpDateForm(instance=request.user.profile)
    context = {
        'p_form': p_form,
    }
    return render(request, 'accounts/profile_update.html', context)


def user_dashboard(request):
    obj = UserBalance.objects.get(user=request.user)
    context = {
        'obj': obj,
    }
    return render(request, 'accounts/user_dashboard.html', context)


def bank_create_view(request):
    form = BanksForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = BanksForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/bank.html', context)



class user_transfer_view(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        object = Transfer.objects.filter(user=self.request.user)
        paginator = Paginator(object, 4)  # Show 4 contacts per page.
        page_number = self.request.GET.get('page')
        item = paginator.get_page(page_number)
        context = {
            'page_obj': item
        }
        return render(self.request, 'accounts/user-transfer.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
