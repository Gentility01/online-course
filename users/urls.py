from django.urls import path
from . import views


urlpatterns = [
    path("register-learner", views.register_learner, name="register_learner"),
    path("login-user", views.login_user, name="login_user"),
    path("logout-user", views.logout_user, name="logout_user"),
    path("register-instructor", views.register_instructor, name="register_instructor"),
]
