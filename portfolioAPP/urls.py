from django.urls import path
from . import views 

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgot-password/',views.ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset-password/<str:token>/',views.ResetPasswordView.as_view(),name='reset_password'),
    
    path('projects/', views.ProjectsListView.as_view(), name='projects'),
    path('experience/', views.ExperiencesListView.as_view(), name='experience'),
    path('skills/', views.SkillsListView.as_view(), name='skills'),

    
  

]