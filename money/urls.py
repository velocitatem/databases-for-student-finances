from .views import get_average_budget

from django.urls import path


urlpatterns = [
    path('average-budget/', get_average_budget, name='average-budget'),
]