from django.urls import path, include

from .views import MakeOrder

urlpatterns = [
    path('order/', MakeOrder.as_view()),
]
