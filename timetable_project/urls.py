"""
URL configuration for timetable_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Correct import in timetable_project/urls.py
from django.contrib import admin
from django.urls import path, include
from timetable_app import views  # Correctly import views from timetable_app
from django.contrib.auth import views as auth_views
from timetable_app.views import custom_login  # Correct import path
from timetable_app.views import custom_logout
from timetable_app.views import homepage
from timetable_app.views import not_authorized

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_schedule/', views.create_schedule, name='create_schedule'),  # Use the views from timetable_app
    path('schedule_list/', views.schedule_list, name='schedule_list'),  # Ensure this view exists or remove if not
    # Include any other views or routes here
    path('edit_schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('clear_schedule/<int:schedule_id>/', views.clear_schedule, name='clear_schedule'),
    path('login/', auth_views.LoginView.as_view(template_name='timetable_app/login.html'), name='login'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('home/', homepage, name='homepage'),
    path('not_authorized/', not_authorized, name='not_authorized'),


]


