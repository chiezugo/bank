# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import RegisterForm, UserAdminChangeForm
from .models import UserTransaction, UserBalance, Deposit, Profile, Bank, Transfer, RequestFund, MasterCard, System

User = get_user_model()

def make_request_fund_approved(modeladmin, request, queryset):
    queryset.update(requested=False, accepted=True)


make_request_fund_approved.short_description = 'Update fund requests to accepted'

class RequestFundAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'requested',
        'accepted',
        'date',
    ]

    list_display_links = [
        'user',
        'amount',
        'requested',
    ]

    list_filter = [
        'user',
        'amount',
        'requested',
        'date'

    ]

    search_fields = [
        'user',
        'amount',
        'requested'

    ]
    actions = [make_request_fund_approved]

class MasterCardAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'code',
        'code1',
        'code2',
        'code3',
        'cvv',
        'sum',
        'date'

    ]

class BankAdmin(admin.ModelAdmin):
    list_display = [
        'bank'

    ]
    list_display_links = [
        'bank'

    ]

    list_filter = [
        'bank'

    ]

    search_fields = [
        'bank'

    ]


class DepositAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'timestamp',
        'balance',
    ]

class TransferAdmin(admin.ModelAdmin):
    list_display = [
        'bank',
        'user',
        'receiver',
        'amount',
        'description',
        'trans_reference',
        'transfer_date'

    ]
    list_display_links = [
        'bank',
        'amount',
        'description',
        'trans_reference',
        'transfer_date'

    ]

    list_filter = [
        'bank',
        'amount',
        'description',
        'trans_reference',
        'transfer_date'

    ]

    search_fields = [
        'bank',
        'amount',
        'description',
        'trans_reference',
        'transfer_date'

    ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'transaction_type',
        'date',
        'trans_reference'
    ]
    list_display_links = [
        'user',
        'transaction_type',
    ]

    list_filter = [
        'transaction_type',
    ]

    search_fields = [
        'user__email',
        'transaction_type'
    ]


class BalanceAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'balance',

    ]

    list_filter = [
        'user',

    ]

    search_fields = [
        'user__email',

    ]



class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'pin'
    ]

class SystemAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'active'
    ]

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm  # update view
    add_form = RegisterForm  # create view
    list_display = ('email', 'full_name', 'admin', 'active', 'staff', 'routing_num', 'ac_num', 'user_ref_id')
    list_filter = ('admin', 'active', 'staff', 'user_ref_id')
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        # ('FULL NAME', {'fields': ('full_name',)}),
        ('permissions', {'fields': ('admin', 'active', 'staff')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'user_ref_id')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(UserTransaction, TransactionAdmin)
admin.site.unregister(Group)
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(System, SystemAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(UserBalance, BalanceAdmin)
admin.site.register(Profile, UserProfileAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(MasterCard, MasterCardAdmin)
admin.site.register(Transfer, TransferAdmin)
admin.site.register(RequestFund, RequestFundAdmin)
