from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
    path('success_login/', views.success_login),
    path('success_registration/', views.success_register),
    path('grades/', views.show_grades),
    path('subjects/', views.show_all_subjects_specific_group),
    path('groups/', views.AllGroups.as_view()),
    path('groups/<int:group_id>/', views.group_detail),
]
