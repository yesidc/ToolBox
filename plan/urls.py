from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('human_touch/', views.human_touch, name='human_touch'),
    path('teaching_material/', views.teaching_material, name='teaching_material'),
    path('organization/', views.organization, name='organization'),
    path('assignment/', views.assignment, name='assignment'),
    path('student_engagement/', views.student_engagement, name='student_engagement'),
    path('discussion/', views.discussion, name='discussion'),
    path('assessment/', views.assessment, name='assessment'),
    path('rules_regulations/', views.rules_regulations, name='rules_regulations'),
   path('idea_overview/', views.idea_overview, name='idea_overview'),
   path('idea_detail/', views.idea_detail, name='idea_detail'),

]
