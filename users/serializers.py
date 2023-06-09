from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(email=self.validated_data['email'], username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get('username_or_email')
        password = attrs.get('password')
        model = User.objects.all()
        if model.filter(email__exact=email_or_username):
            if email_or_username and password:
                user = authenticate(email=email_or_username, password=password)
                if user:
                    if not user.is_active:
                        msg = 'User users is disabled.'
                        raise serializers.ValidationError(msg, code='authorization')
                    attrs['user'] = user
                    return attrs
                else:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg, code='authorization')
        elif email_or_username and password:
            try:
                email = model.filter(username__exact=email_or_username).values('email').first()
                user = authenticate(email=email.get('email'), password=password)
            except AttributeError:
                raise serializers.ValidationError('This username or email does not exist!',
                                                  code='authorization')

            if user:
                if not user.is_active:
                    msg = 'User users is disabled.'
                    raise serializers.ValidationError(msg, code='authorization')
                attrs['user'] = user
                return attrs
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "email_or_username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')


class UserSerializersList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'date']


class SocialSerializersList(serializers.ModelSerializer):
    access_token = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_user_token')

    def get_user_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj.user)
        return token.key

    class Meta:
        model = User
