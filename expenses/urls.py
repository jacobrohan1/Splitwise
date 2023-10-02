from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'expenses', views.ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<str:user_id>/expenses/', views.check_user_balance, name='user_expenses'),
    path('show-balances/', views.show_balances, name='show_balances'),
    path('split-expense/', views.split_expense, name='split_expense'),
]
