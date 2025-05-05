from rest_framework import serializers
from django.contrib.auth import get_user_model
CustomUser=get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email',  'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user
class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [ 'email', 'first_name','last_name', 'password', 'profile_image','address','phone',]

    def update(self, instance, validated_data):
        if password := validated_data.pop('password', None):
            instance.set_password(password)
        return super().update(instance, validated_data)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField(min_length=6)