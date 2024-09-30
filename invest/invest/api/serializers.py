from builtins import len

from django.conf import settings
from rest_framework import serializers

from .models import Profile, UserTransaction


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ["id", 'full_name',
                  'email',
                  'location',
                  ]

    def get_is_following(self, obj):
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.follower.all()
        return is_following

    def get_full_name(self, obj):
        return obj.user.full_name

    def get_email(self, obj):
        return obj.user.email


class UserTransactionSerializer(serializers.Serializer):
    user = ProfileSerializer(source='user.profile', read_only=True)
    transaction_type = serializers.CharField(read_only=True)
    approved = serializers.CharField(read_only=True)
    amount = serializers.SerializerMethodField(read_only=True)

    def get_approved(self, obj):
        return obj.approved

    def get_amount(self, obj):
        return obj.amount

    def get_transaction_type(self, obj):
        return obj.transaction_type

    class Meta:
        model = UserTransaction
        fields = ['user', 'id', 'date', 'transaction_type', 'approved']


class UserTransactionCreateSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(source='user.profile', read_only=True)
    transaction_type = serializers.SerializerMethodField(read_only=True, default='Deposit')

    class Meta:
        model = UserTransaction
        fields = ['user', 'id', 'date', 'transaction_type', 'amount']


    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("enter a real amount")
        return value

    def get_transaction_type(self, obj):
        return obj.transaction_type
