from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('error', views.index, name='index'),

    path('network/<str:project_id>', views.projectMainNetwork, name='project-main-network'),

]