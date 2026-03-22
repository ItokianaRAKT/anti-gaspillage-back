from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name',
            'tel1_user', 'tel2_user',
            'address_user', 'profile_pic_user',
        )
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id_user', 'username', 'email',
            'first_name', 'last_name',
            'tel1_user', 'tel2_user',
            'address_user', 'profile_pic_user',
            'saved_in_90_days', 'total_product_saved',
        )
        read_only_fields = ('id_user', 'username', 'saved_in_90_days', 'total_product_saved')


class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer pour le profil public — sans infos sensibles"""
    class Meta:
        model = User
        fields = (
            'id_user', 'username',
            'first_name', 'last_name',
            'profile_pic_user',
            'saved_in_90_days', 'total_product_saved',
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Les mots de passe ne correspondent pas."})
        return attrs