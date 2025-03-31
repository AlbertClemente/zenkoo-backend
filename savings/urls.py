from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views.user_views import UserRegisterView
from .views.income_views import IncomeListCreateView
from .views.expense_views import ExpenseListCreateView
from .views.category_views import CategoryListCreateView
from .views.savinggoal_views import SavingGoalListCreateView
from .views.reflection_views import ReflectionListCreateView
from .views.notification_views import NotificationListCreateView, NotificationMarkReadView
from .views.cripto_views import CriptoListView, CriptoUpdateView

urlpatterns = [
    path('users/register/', UserRegisterView.as_view(), name='user-register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('incomes/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('saving-goals/', SavingGoalListCreateView.as_view(), name='savinggoal-list-create'),
    path('reflections/', ReflectionListCreateView.as_view(), name='reflection-list-create'),
    path('notifications/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('notifications/<uuid:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('criptos/', CriptoListView.as_view(), name='cripto-list'),
    path('criptos/update/', CriptoUpdateView.as_view(), name='cripto-update'),
]
