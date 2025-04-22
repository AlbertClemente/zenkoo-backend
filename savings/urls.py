from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views.user_auth_views import CustomTokenObtainPairView, CustomTokenRefreshView
from .views.user_views import UserRegisterView, UserProfileView, ChangePasswordView
from .views.income_views import IncomeListCreateView, IncomeDetailView
from .views.expense_views import ExpenseListCreateView, ExpenseDetailView
from .views.category_views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView
from .views.savinggoal_views import SavingGoalListCreateView, SavingGoalDetailView
from .views.reflection_views import ReflectionListCreateView, ReflectionRetrieveUpdateDestroyView
from .views.notification_views import NotificationListCreateView, NotificationDeleteAllView, NotificationRetrieveDeleteView, NotificationMarkReadView, unread_notifications_count
from .views.cripto_views import CriptoListView, CriptoUpdateView
from .views.montly_plan_views import MonthlyPlanCurrentView, MonthlyPlanCreateUpdateView, MonthlyPlanRetrieveUpdateView
from .views.admin import ModelInfoView, PlatformStatsView
from .views.admin import RetrainModelView

urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='user-register'),
    path('users/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('users/change-password/', ChangePasswordView.as_view(), name='user-change-password'),
    path('incomes/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('incomes/<uuid:pk>/', IncomeDetailView.as_view(), name='income-detail'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<uuid:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<uuid:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('saving-goals/', SavingGoalListCreateView.as_view(), name='savinggoal-list-create'),
    path('saving-goals/<uuid:pk>/', SavingGoalDetailView.as_view(), name='savinggoal-detail'),
    path('reflections/', ReflectionListCreateView.as_view(), name='reflection-list-create'),
    path('reflections/<uuid:pk>/', ReflectionRetrieveUpdateDestroyView.as_view(), name='reflection-detail'),
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/delete/all/', NotificationDeleteAllView.as_view(), name='notification-delete-all'),
    path('notifications/<uuid:pk>/', NotificationRetrieveDeleteView.as_view(), name='notification-detail-delete'),
    path('notifications/<uuid:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('notifications/unread/count/', unread_notifications_count, name='notification-unread-count'),
    path('criptos/', CriptoListView.as_view(), name='cripto-list'),
    path('criptos/update/', CriptoUpdateView.as_view(), name='cripto-update'),
    path('monthly-plan/current/', MonthlyPlanCurrentView.as_view(), name='monthly-plan-current'),
    path('monthly-plan/', MonthlyPlanCreateUpdateView.as_view(), name='monthly-plan-create-update'),
    path('monthly-plan/<uuid:pk>/', MonthlyPlanRetrieveUpdateView.as_view(), name='monthly-plan-detail'),
    path('admin/model-info/', ModelInfoView.as_view(), name='model-info'),
    path("admin/stats/", PlatformStatsView.as_view(), name='platform-stats'),
    path("ml/retrain/", RetrainModelView.as_view(), name="retrain-model"),
]
