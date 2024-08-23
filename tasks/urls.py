from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, AssignmentViewSet, dashboard, create_task, assign_task, complete_task

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('create_task/', create_task, name='create_task'),
    path('complete_task/<int:assignment_id>/', views.complete_task, name='complete_task'),
    path('task_details/<int:assignment_id>/', views.task_details, name='task_details'),
    path('assign_task/<int:task_id>/', assign_task, name='assign_task'),
]