from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction

from authorize.models import User, UserToken, Profile
from school.models import School


class LoginWriteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, help_text='Email')
    password = serializers.CharField(required=True, max_length=30, help_text='Password')


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    surname = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    birthdate = serializers.DateField(required=True)
    # school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), required=True)

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).count() > 0:
            raise ValidationError({'status': 0, 'data': 'Already exists'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        # try:
        #     administrator = KassaRole.objects.get(unique_number=1)
        # except KassaRole.DoesNotExist:
        #     raise ValidationError({'status': 2, 'error': 'Add platform permission with unique key'})
        # company = Company.objects.create(
        #     bin_iin=validated_data.get('bin_iin'),
        #     custom_reg=True,
        #     pin_prog="0000",
        #     pin_kassa_in="0000",
        #     pin_close_shift="0000",
        #     pin_rmni="0000",
        # )
        user = User.objects.create(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            surname=validated_data.get('surname'),
            birthdate=validated_data.get('birthdate')
        )
        user.set_password(validated_data.get('password'))

        # TODO is_active delete
        user.is_active = True

        user.save()
        # Profile.objects.create(
        #     user=user,
        #     school=validated_data.get('school')
        # )
        #
        # company_user = CompanyUser.objects.create(
        #     company=company,
        #     user=user
        # )
        # Department.objects.get_or_create(company=company, name_ru='Секция 1', name_kz='Секция 1', code='1000',
        #                                  is_active=True)
        # company_user.roles.add(administrator)
        # company_user.save()
        return user


class ForgetPasswordWriteSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    code = serializers.CharField(max_length=50, required=False, default=None)


class ActivateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=120, required=True)


class UserResponseSerializer(serializers.ModelSerializer):
    # photo = serializers.ImageField(use_url=False)
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, instance):
        if self.context.get('token'):
            return self.context.get('token')
        return instance.auth_tokens.last().key

    class Meta:
        model = User
        fields = ('email', 'name', 'auth_token', 'id')


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'birthdate', 
                    'phone', 'email')





#------------------------------------------------
class TestSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)