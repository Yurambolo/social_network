from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Post, Like


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super(UserTokenObtainPairSerializer, cls).get_token(user)
        token['is_staff'] = user.is_staff

        user.last_login = timezone.now()
        user.save()
        return token

    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            pass

        try:
            data = {}
            request_data = request.data
            if ("email" in request_data and "password" in request_data):
                user = User.objects.filter(email=request_data['email']).first()
                if user.check_password(request_data['password']):
                    self.user = user
            else:
                raise serializers.ValidationError({"username/password": "These fields are required"})

            refresh = self.get_token(self.user)
            user.last_login = timezone.now()
            user.save()

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data

        except:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'name')
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=False, allow_blank=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'name')
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate(self, attrs):
        if 'password' in attrs and attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'password' in validated_data and validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'article', 'content']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user']
