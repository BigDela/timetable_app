from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from timetable_app.views import custom_login  # Correct import path
from timetable_app.views import custom_logout
from timetable_app.views import not_authorized
from timetable_app.views import homepage
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('schedule_list/', views.schedule_list, name='schedule_list'),  # Placeholder for a schedule list view
    path('edit_schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('clear_schedule/<int:schedule_id>/', views.clear_schedule, name='clear_schedule'),
    path('login/', auth_views.LoginView.as_view(template_name='timetable_app/login.html'), name='login'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('not_authorized/', not_authorized, name='not_authorized'),
    path('home/', homepage, name='homepage'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login')

]


