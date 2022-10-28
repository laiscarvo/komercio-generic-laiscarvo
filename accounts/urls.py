from unittest.mock import patch
from django.urls import path

from . import views

urlpatterns = [
    path("accounts/", views.AccountsView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("accounts/newest/<int:num>/", views.AccountListView.as_view()),
    path("accounts/<pk>/", views.AccountDetailView.as_view()),
    path("accounts/<pk>/management/", views.AccountUpdateView.as_view()),
]
