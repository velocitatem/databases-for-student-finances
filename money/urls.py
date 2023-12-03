from .views import get_average_budget, get_user_transactions

from django.urls import path

urlpatterns = [
    path('average-budget/', get_average_budget, name='average-budget'),
    path('user-transactions/<str:user_id>/', get_user_transactions, name='user-transactions'),
]