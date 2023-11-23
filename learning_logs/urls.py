"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Головна сторінка.
    path('', views.index, name='index'),
    # Сторінка, що відображає всі теми.
    path('topics/', views.topics, name='topics'),
    # Сторінка, присвячена окремій темі.
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Сторінка дял додавання нової теми.
    path('new_topic/', views.new_topic, name='new_topic'),
]