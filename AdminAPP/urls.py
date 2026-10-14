from django.urls import path
from . import views 

app_name = 'AdminAPP'

urlpatterns = [
    path('', views.dashboardListView.as_view(), name='dashboard'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('add_projects/', views.add_projects, name='add_projects'),
    path('add_experiences/', views.add_experiences, name='add_experiences'),
    path('add_skills/', views.add_skills, name='add_skills'),
    

    path('projects/', views.ProjectsListView.as_view(), name='projects'),
    path('update/<int:pk>/',views.ProjectUpdateView.as_view(),name='project_edit'),
    path('view_project/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('project_del/<int:pk>', views.ProjectDeleteView.as_view(), name='project_del'),

    path('experiences/', views.ExperiencesListView.as_view(), name='experiences'),
    path('experience_edit/<int:pk>/', views.ExperienceUpdateView.as_view(), name='experience_edit'),
    path('experience_detail/<int:pk>/', views.ExperienceDetailView.as_view(), name='experience_detail'),
    path('experience_del/<int:pk>/', views.ExperienceDeleteView.as_view(), name='experience_del'),

    path('skills/', views.SkillsListView.as_view(), name='skills'),
    path('skill_edit/<int:pk>/', views.SkillUpdateView.as_view(), name='skill_edit'),
    path('skill_del/<int:pk>/', views.SkillDeleteView.as_view(), name='skill_del'),

    path('messages/', views.MessageListView.as_view(), name='messages'),
    path('messages/<int:pk>/',views.MessageDetailView.as_view(), name='view_message'),
    path('messages/<int:pk>/read/',views.MarkMessageReadView.as_view(),name='mark_message_read' ),
    path('message_del/<int:pk>/', views.MessageDeleteView.as_view(), name='message_del'),

    path('logout/', views.LogoutView.as_view(), name='logout'),
    
]
