from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("authorized", views.AuthorizedView.as_view(), name="authorized"),
    path("login", views.LoginInterfaceView.as_view(), name="login"),
    path("logout", views.LogoutInterfaceView.as_view(), name="logout"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("user/edit/<int:pk>", views.UpdateView.as_view(), name="update"),
    # path("user/delete/<int:pk>", views.CustomUserDeleteView.as_view(), name="delete"),
    path("user/<int:pk>", views.CustomUserDetailView.as_view(), name="user-detail"),
    path("api/v1/users/", views.CustomUserApiList.as_view(), name="user-list"),
    path(
        "api/v1/users/<int:pk>/",
        views.CustomUserApiDetail.as_view(),
        name="user-detail",
    ),
    path(
        "api/v1/users/create",
        views.CustomUserCreateAPIView.as_view(),
        name="user-create",
    ),
    # path(
    #     "api/v1/users/update/<int:pk>",
    #     views.CustomUserApiDetail.as_view(),
    #     name="user-update",
    # ),
    # path(
    #     "api/v1/users/delete/<int:pk>",
    #     views.CustomUserApiDetail.as_view(),
    #     name="user-delete",
    # ),
]
