from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_document/<str:file_id>/', views.view_document, name='view_document'),
    path('logout/', views.logout_view, name='logout'),
    # Add other URL patterns
] 
