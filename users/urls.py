from django.urls import path
from . import views


urlpatterns = [
    path('', views.profiles,name="profiles"),
    path('register/', views.registerUser,name="register"),
    path('login/', views.loginUser,name="login"),
    path('logout/', views.logoutUser,name="logout"),
    path('profile/<str:id>', views.profile,name="profile"),
    path('account/', views.userAccount,name="account"),
    path('editAccount/', views.editAccount,name="editAccount"),

]
