from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from services.generator import CodeGenerator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )

    def validate(self, attrs):
        password = attrs.get("password")
        try:
            user = User.objects.get(email=attrs.get("email"))
        except:
            raise serializers.ValidationError({"error": "Email yanlisdir."})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Sifre yanlisdir."})
        if not user.is_active:
            raise serializers.ValidationError({"error": "Bu hesab aktif deyil."})
        return super().validate(attrs)

    def get_user(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        return authenticate(email=email, password=password)

    def create(self, validated_data):
        return self.get_user()

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return repr_


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "uuid",
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirm"
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Bu mail artiq qeydiyyatda var."})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error": "Bu username artiq movcuddur"})
        if len(password) < 8:
            raise serializers.ValidationError({"error": "Sifrenin uzunlugu 8 den kicik ola bilmez."})
        if not password == password_confirm:
            raise serializers.ValidationError({"error": "Sifreler arasinda ziddiyet var."})
        if not any(_.isdigit() for _ in password):
            raise serializers.ValidationError({"error": "Sifrede en az bir reqem olmalidir"})
        if not any(_.isupper() for _ in password):
            raise serializers.ValidationError({"error": "Sifrede en az bir boyuk herif olmalidir."})
        return super().validate(attrs)

    def get_uuid(self, obj):
        return urlsafe_base64_encode(smart_bytes(obj.id))

    def create(self, validated_data):
        password = validated_data.pop("password_confirm")
        user = User.objects.create(**validated_data, is_active=False)
        user.set_password(password)
        user.activation_code = CodeGenerator.create_user_activation_code(size=6, model_=User)
        user.save()
        # send mail
        send_mail(
            "Pastry World | Activation",
            f"Your activation code: {user.activation_code}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=True
        )
        return user


class ActivationCheckSerializer(serializers.ModelSerializer):
    activation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "activation_code",
        )

    def validate(self, attrs):
        user = self.instance
        code = attrs.get("activation_code")

        if not user.activation_code == code:
            raise serializers.ValidationError({"error": "Code is wrong."})

        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.activation_code = None
        instance.save()
        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return repr_


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "email"
        )

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Bu mail ile user movcud deyil."})

        return super().validate(attrs)

    def get_uuid(self, obj):
        return urlsafe_base64_encode(smart_bytes(obj.id))

    def create(self, validated_data):
        email = validated_data.get("email")
        user = User.objects.get(email=email)
        user.activation_code = CodeGenerator.create_user_activation_code(size=6, model_=User)
        user.save()
        # send mail
        send_mail(
            "Pastry World | Reset Password",
            f"Your reset code: {user.activation_code}",
            settings.EMAIL_HOST_USER,
            [email,],
            fail_silently=True
        )
        return user


class ResetPasswordCheckSerializer(serializers.ModelSerializer):
    reset_code = serializers.CharField(required=True, write_only=True)
    uuid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "reset_code",
        )

    def get_uuid(self, obj):
        return urlsafe_base64_encode(smart_bytes(obj.id))

    def validate(self, attrs):
        user = self.instance
        reset_code = attrs.get("reset_code")

        if not user.activation_code == reset_code:
            raise serializers.ValidationError({"error": "Code is wrong."})

        return super().validate(attrs)


class ResetPasswordCompleteSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})
    new_password_confirm = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = (
            "email",
            "new_password",
            "new_password_confirm"
        )
        extra_kwargs = {
            "email": {"read_only": True}
        }

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")

        if len(new_password) < 8:
            raise serializers.ValidationError({"error": "Sifrenin uzunlugu 8 den kicik ola bilmez."})
        if not new_password == new_password_confirm:
            raise serializers.ValidationError({"error": "Sifreler arasinda ziddiyet var."})
        if not any(_.isdigit() for _ in new_password):
            raise serializers.ValidationError({"error": "Sifrede en az bir reqem olmalidir"})
        if not any(_.isupper() for _ in new_password):
            raise serializers.ValidationError({"error": "Sifrede en az bir boyuk herif olmalidir."})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        new_password = validated_data.get("new_password")
        instance.set_password(new_password)
        instance.save()
        return instance

    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        token = RefreshToken.for_user(instance)
        repr_["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token)
        }
        return repr_


