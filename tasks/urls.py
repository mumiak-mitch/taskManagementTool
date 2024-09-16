from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('projects_list/', views.project_list, name='project_list'),
    path('add_project/', views.add_project, name='add_project'),
    path('projects/<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),

    path('add_task/<int:project_id>/tasks/add/', views.add_task, name='add_task'),
    path('task_list/<int:project_id>/', views.task_list, name='task_list'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    path('tasks/<int:task_id>/priority/<int:priority>/', views.update_task_priority, name='update_task_priority'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]
