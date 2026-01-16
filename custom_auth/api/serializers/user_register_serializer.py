from django.core import validators
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    password = serializers.CharField(write_only=True, required=True, validators=[
        validators.MinLengthValidator(8),
        validators.RegexValidator(
            regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])',
            message='Şifre en az bir büyük harf, bir küçük harf ve bir sayı içermelidir.'
        )
    ])
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        super().validate(data)

        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                ['Şifreler eşleşmelidir.'])

        return data

    def create(self, validated_data):
        try:
            obj = super().create(validated_data)
            obj.is_active = False
            obj.save()
            return obj
        finally:
            del obj

    class Meta:
        model = User
        fields: tuple = ('username', 'email', 'password', 'password_confirm')

