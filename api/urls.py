from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns=[

    path('',views.getRoutes,name='api'),
    path('projects/',views.getProjects,name='pro'),
    path('projects/<str:pk>',views.getProject,name='pr'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]