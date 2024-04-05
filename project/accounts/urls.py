from django.urls import path
from .views import CustomConfirmEmailView

urlpatterns = [
    path('confirm/', CustomConfirmEmailView.as_view(), name='confirm'),
]