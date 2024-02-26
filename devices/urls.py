from django.urls import path
from . import views

urlpatterns = [
    path('device/<str:project_id>/createdevice/<str:template_id>', views.CreateDevice, name='create-device'),

    path('device/<str:project_id>/<str:device_id>/view', views.deviceIndex, name='device-view'),
    path('device/<str:project_id>/<str:device_id>/delete', views.deviceDelete, name='device-delete'),
    
    path('device/<str:project_id>/<str:device_id>/start', views.deviceStart, name='device-start'),
    path('device/<str:project_id>/<str:device_id>/reload', views.deviceReload, name='device-reload'),
    path('device/<str:project_id>/<str:device_id>/suspend', views.deviceSuspend, name='device-suspend'),
    path('device/<str:project_id>/<str:device_id>/stop', views.deviceStop, name='device-stop'),
    
    path('device/<str:project_id>/<str:device_id>/running_config', views.deviceRunningConfig, name='device-running-config'),
    path('device/<str:project_id>/<str:device_id>/startup_config', views.deviceStartupConfig, name='device-startup-config'),
    path('device/<str:project_id>/<str:device_id>/ip_routes', views.deviceIpRoute, name='device-ip-routes'),
    path('device/<str:project_id>/<str:device_id>/ping/<str:ip_address>', views.devicePingIpAddress, name='device-ping-ip-address'),
    path('device/<str:project_id>/<str:device_id>/copy_running_to_startup', views.deviceCopyRunningToStartup, name='device-copy-running-to-startup'),
    path('device/<str:project_id>/<str:device_id>/vlans', views.deviceGetVlans, name='device-get-vlans'),

]