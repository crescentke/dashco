from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from dashcodrf.models import Client, RoutePlan, RoutePlanLog

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    token = CharField(allow_blank=True, read_only=True)
    error = CharField(allow_blank=True, read_only=True)
    id = CharField(allow_blank=True, read_only=True)
    username = CharField()
    password = CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(
            Q(username=username)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
            if user_obj:
                if not user_obj.check_password(password):
                    data['error'] = 'Incorrect password. Please try again'
                    data['token'] = 'False'
                else:
                    data['token'] = 'True'
                    data['id'] = user_obj.id
        else:
            data['token'] = 'False'
            data['error'] = 'Username is not valid'

        return data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'dob', 'national_id', 'slug']


class RoutePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePlan
        fields = ['title', 'user', 'visit_date', 'location', 'slug']


class RoutePlanLogSerializer(serializers.Serializer):
    client = CharField()
    user = CharField()
    location_lat = CharField()
    location_lon = CharField()
    branch = CharField()
    action = CharField()

    def validate(self, data):
        return data
