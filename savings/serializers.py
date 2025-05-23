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

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual no es correcta.")
        return value

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

    monthly_plan = serializers.PrimaryKeyRelatedField(queryset=MonthlyPlan.objects.all(), required=False)

    class Meta:
        model = Reflection
        fields = [
            'id', 'title', 'content', 'created_at', 'updated_at', 'user', 'monthly_plan'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate_content(self, value):
        if not value.strip():  # Si el contenido está vacío o sólo tiene espacios
            raise serializers.ValidationError("El contenido no puede estar vacío")
        return value

    def validate_monthly_plan(self, value):
        if value:
            try:
                MonthlyPlan.objects.get(id=value)
            except MonthlyPlan.DoesNotExist:
                raise serializers.ValidationError("El plan mensual con el ID proporcionado no existe.")
        return value

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
    income = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    expense = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    real_savings = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    reflection = ReflectionSerializer(read_only=True)

    reflection_pk = serializers.PrimaryKeyRelatedField(
        queryset=Reflection.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='reflection'
    )

    class Meta:
        model = MonthlyPlan
        fields = [
            'id', 'month', 'reserved_savings', 'reflection', 'reflection_pk',
            'created_at', 'income', 'expense', 'real_savings'
        ]
        read_only_fields = ['id', 'month', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['income'] = str(self.context.get('income', '0.00'))
        data['expense'] = str(self.context.get('expense', '0.00'))
        data['real_savings'] = str(self.context.get('real_savings', '0.00'))

        # Esto asegura que si la reflexión es None, se devuelve como tal
        if instance.reflection is None:
            data['reflection'] = None

        return data

class PredictCategoryInputSerializer(serializers.Serializer):
    text = serializers.CharField(help_text="Texto del gasto o ingreso para categorizar")
