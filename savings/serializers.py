from rest_framework import serializers
from .models import User, Cripto, Income, Expense, SavingGoal, Reflection, Category, Notification

class UserSerializer(serializers.ModelSerializer):
    """Serializer para mostrar datos de usuario (sin contraseña)"""
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'email', 'profile_picture', 'date_of_birth', 'created_at', 'updated_at',
            'is_active', 'is_staff'
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
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer para registrar y ver gastos del usuario"""

    class Meta:
        model = Expense
        fields = [
            'id', 'amount', 'date', 'type', 'created_at', 'updated_at', 'user', 'category'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class SavingGoalSerializer(serializers.ModelSerializer):
    """Serializer para crear, listar y actualizar metas de ahorro"""

    class Meta:
        model = SavingGoal
        fields = [
            'id', 'target_amount', 'current_amount', 'deadline', 'status', 'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ReflectionSerializer(serializers.ModelSerializer):
    """Serializer para crear y ver reflexiones personales del usuario"""

    class Meta:
        model = Reflection
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class CategorySerializer(serializers.ModelSerializer):
    """Serializer para gestionar categorías y subcategorías"""

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'type', 'created_at', 'updated_at', 'user', 'parent'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para mostrar y gestionar notificaciones del usuario"""

    class Meta:
        model = Notification
        fields = [
            'id', 'message', 'is_read', 'created_at', 'user'
        ]
        read_only_fields = ['id', 'created_at']
