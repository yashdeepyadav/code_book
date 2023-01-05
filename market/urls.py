
from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects,name="projects"),
    path('project/<str:pk>/',views.project,name="project"),
    path('addProject/', views.addProject,name="addProject"),
    path('updateProject/<str:pk>/', views.updateProject,name="updateProject"),
    path('deleteProject/<str:pk>/', views.deleteProject,name="deleteProject"),
]
