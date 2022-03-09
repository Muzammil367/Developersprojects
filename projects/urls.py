from django.urls import path
from projects import views

app_name = 'projects'

urlpatterns = [
    path('',views.projectAll,name='project-all'),
    path('project/<str:pk>/',views.project,name = 'project'),
    path('create-project/',views.createProject,name='create-project'),
    path('update-project/<str:pk>/',views.updateProject,name='update-project'),
    path('delete-project/<str:pk>/',views.deleteProject,name='delete-project'),
    ]