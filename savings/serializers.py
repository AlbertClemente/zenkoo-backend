from rest_framework import serializers
from .models import User, Cripto, Income, Expense, SavingGoal, Reflection, Category, Notification, MonthlyPlan

from .ml.predict import predict_category # IA Categorización

class UserSerializer(serializers.ModelSerializer):
    """Serializer para mostrar datos de usuario (sin contraseña)"""
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'profile_picture', 'date_of_birth', 'created_at', 'updated_at',
            'is_active', 'is_staff', 'is_superuser'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer para registrar nuevos usuarios"""
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'password', 'profile_picture', 'date_of_birth'
        ]
        extra_kwargs = {
            'profile_picture': {'required': False, 'allow_blank': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            profile_picture=validated_data.get('profile_picture', ''),
            date_of_birth=validated_data.get('date_of_birth')
        )
        return user

class CriptoSerializer(serializers.ModelSerializer):
    """Serializer para ver criptomonedas"""
    class Meta:
        model = Cripto
        fields = ['id', 'name', 'symbol', 'price', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class IncomeSerializer(serializers.ModelSerializer):
    """Serializer para registrar y ver ingresos del usuario"""

    class Meta:
        model = Income
        fields = [
            'id', 'amount', 'date', 'type', 'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class ExpenseSerializer(serializers.ModelSerializer):
    print("🔁 Cargando ExpenseSerializer actualizado")

    category = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'type', 'created_at', 'updated_at', 'user', 'category'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate_category(self, value):
        request = self.context.get('request')
        user = request.user if request else None

        if not value:
            return None  # Permitimos categoría vacía

        if user:
            category, _ = Category.objects.get_or_create(
                name=value.strip(),
                type='expense',
                user=user
            )
            return category

        raise serializers.ValidationError("Categoría no válida.")

    def create(self, validated_data):
        print("✅ ExpenseSerializer ACTIVO")
        return super().create(validated_data)

class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = [
            'id', 'title', 'target_amount', 'current_amount', 'deadline', 'status',
            'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

class ReflectionSerializer(serializers.ModelSerializer):
    """Serializer para crear y ver reflexiones personales del usuario"""

    class Meta:
        model = Reflection
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

class CategorySerializer(serializers.ModelSerializer):
    """Serializer para gestionar categorías y subcategorías"""

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'type', 'created_at', 'updated_at', 'user', 'parent'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        type_ = data.get('type')
        instance = getattr(self, 'instance', None)

        qs = Category.objects.filter(user=user, name=name, type=type_)
        if instance:
            qs = qs.exclude(pk=instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Ya existe una categoría con ese nombre y tipo.")
        return data

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para mostrar y gestionar notificaciones del usuario"""

    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'is_read', 'created_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'user']

class MonthlyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyPlan
        fields = ['id', 'month', 'reserved_savings', 'reflection', 'created_at']
