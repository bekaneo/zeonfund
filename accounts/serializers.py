from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from cases.serializers import CaseSerializer
from fund import settings


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'is_staff', 'activation_code']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cases'] = CaseSerializer(instance.case.all(), many=True).data
        return representation


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number']


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email is already exists')
        return email

    def validate(self, attrs):
        attrs['email'] = attrs.pop('email')
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        return super().validate(attrs)

    def create(self):
        user = User.objects.create_user(**self.validated_data)
        user.create_activation_code()
        user.send_activation_code()


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=4)

    def validate_login(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email does not exists')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Password is not valid')
        return super().validate(attrs)


class RestorePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_login(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email does not exists')
        return email

    def send_verification_code(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email does not exists')
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            subject='Activation',
            message=f'?????? ?????? {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )


class RestorePasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField()
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('activation_code')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User with this email and activation code not found')
        return super().validate(attrs)

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4)
    new_password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
        return password

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        password_confirm = attrs.get('password_confirm')
        if new_password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        return super().validate(attrs)

    def set_new_password(self):
        user = self.context['request'].user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()
